import cv2
import torch
import numpy as np
import torch.nn.functional as F


def iou(box1, box2):
    def area_box(box):
        return (box[2] - box[0]) * (box[3] - box[1])

    left = max(box1[0], box2[0])
    top = max(box1[1], box2[1])
    right = min(box1[2], box2[2])
    bottom = min(box1[3], box2[3])
    cross = max((right - left), 0) * max((bottom - top), 0)
    union = area_box(box1) + area_box(box2) - cross
    if cross == 0 or union == 0:
        return 0
    return cross / union


def NMS(boxes, iou_thres):
    remove_flags = [False] * len(boxes)

    keep_boxes = []
    for i, ibox in enumerate(boxes):
        if remove_flags[i]:
            continue

        keep_boxes.append(ibox)
        for j in range(i + 1, len(boxes)):
            if remove_flags[j]:
                continue

            jbox = boxes[j]
            if ibox[5] != jbox[5]:
                continue
            if iou(ibox, jbox) > iou_thres:
                remove_flags[j] = True
    return keep_boxes


def postprocess(pred, conf_thres=0.25, iou_thres=0.45):
    # 输入是模型推理的结果，即8400个预测框
    # 1,8400,116 [cx,cy,w,h,class*80,32]
    boxes = []
    for item in pred[0]:
        cx, cy, w, h = item[:4]
        label = item[4:-32].argmax()
        confidence = item[4 + label]
        if confidence < conf_thres:
            continue
        left = cx - w * 0.5
        top = cy - h * 0.5
        right = cx + w * 0.5
        bottom = cy + h * 0.5
        boxes.append([left, top, right, bottom, confidence, label, *item[-32:]])

    boxes = sorted(boxes, key=lambda x: x[4], reverse=True)

    return NMS(boxes, iou_thres)


def crop_mask(masks, boxes):
    # masks -> n, 160, 160  原始 masks
    # boxes -> n, 4         检测框，映射到 160x160 尺寸下的
    n, h, w = masks.shape
    x1, y1, x2, y2 = torch.chunk(boxes[:, :, None], 4, 1)  # x1 shape(n,1,1)
    r = torch.arange(w, device=masks.device, dtype=x1.dtype)[
        None, None, :
    ]  # rows shape(1,1,w)
    c = torch.arange(h, device=masks.device, dtype=x1.dtype)[
        None, :, None
    ]  # cols shape(1,h,1)

    return masks * ((r >= x1) * (r < x2) * (c >= y1) * (c < y2))


def process_mask(protos, masks_in, bboxes, shape, upsample=False):
    # protos   -> 32, 160, 160 分割头输出
    # masks_in -> n, 32        检测头输出的 32 维向量，可以理解为 mask 的权重
    # bboxes   -> n, 4         检测框
    # shape    -> 640, 640     输入网络中的图像 shape
    # unsample 一个 bool 值，表示是否需要上采样 masks 到图像的原始形状
    c, mh, mw = protos.shape  # CHW
    ih, iw = shape
    # 矩阵相乘 nx32 @ 32x(160x160) -> nx(160x160) -> sigmoid -> nx160x160
    masks = (
        (masks_in.float() @ protos.float().view(c, -1)).sigmoid().view(-1, mh, mw)
    )  # CHW

    downsampled_bboxes = bboxes.clone()
    downsampled_bboxes[:, 0] *= mw / iw
    downsampled_bboxes[:, 2] *= mw / iw
    downsampled_bboxes[:, 3] *= mh / ih
    downsampled_bboxes[:, 1] *= mh / ih

    masks = crop_mask(masks, downsampled_bboxes)  # CHW
    if upsample:
        masks = F.interpolate(masks[None], shape, mode="bilinear", align_corners=False)[
            0
        ]  # CHW
    return masks.gt_(0.5)


def hsv2bgr(h, s, v):
    h_i = int(h * 6)
    f = h * 6 - h_i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    r, g, b = 0, 0, 0

    if h_i == 0:
        r, g, b = v, t, p
    elif h_i == 1:
        r, g, b = q, v, p
    elif h_i == 2:
        r, g, b = p, v, t
    elif h_i == 3:
        r, g, b = p, q, v
    elif h_i == 4:
        r, g, b = t, p, v
    elif h_i == 5:
        r, g, b = v, p, q

    return int(b * 255), int(g * 255), int(r * 255)


def random_color(id):
    h_plane = (((id << 2) ^ 0x937151) % 100) / 100.0
    s_plane = (((id << 3) ^ 0x315793) % 100) / 100.0
    return hsv2bgr(h_plane, s_plane, 1)


def letterbox_yolo(
    img,
    new_shape=(640, 640),
    color=(114, 114, 114),
    auto=False,
    scaleFill=False,
    scaleup=True,
):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 64), np.mod(dh, 64)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(
        img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
    )  # add border
    return img, ratio, (dw, dh)


def scale_image(im1_shape, masks, im0_shape, ratio_pad=None):
    """
    Takes a mask, and resizes it to the original image size

    Args:
      im1_shape (tuple): model input shape, [h, w]
      masks (torch.tensor): [h, w, num]
      im0_shape (tuple): the original image shape
      ratio_pad (tuple): the ratio of the padding to the original image.

    Returns:
      masks (torch.tensor): The masks that are being returned.
    """

    gain = min(
        im1_shape[0] / im0_shape[0], im1_shape[1] / im0_shape[1]
    )  # gain  = old / new
    pad = (
        (im1_shape[1] - im0_shape[1] * gain) / 2,
        (im1_shape[0] - im0_shape[0] * gain) / 2,
    )  # wh padding
    top, left = int(pad[1]), int(pad[0])  # y, x
    bottom, right = int(im1_shape[0] - pad[1]), int(im1_shape[1] - pad[0])
    if len(masks.shape) < 2:
        raise ValueError(
            f'"len of masks shape" should be 2 or 3, but got {len(masks.shape)}'
        )
    masks = masks.permute(1, 2, 0).contiguous()
    masks = masks[top:bottom, left:right]
    # masks = masks.permute(2, 0, 1).contiguous()
    # masks = F.interpolate(masks[None], im0_shape[:2], mode='bilinear', align_corners=False)[0]
    masks = cv2.resize(masks.cpu().numpy(), (im0_shape[1], im0_shape[0]))

    if len(masks.shape) == 2:
        masks = masks[:, :, None]
    return masks


def draw_bbox(bbox, img0, color, wt):
    # det_result_str = ''
    for idx, class_id in enumerate(bbox[:, 5]):
        if float(bbox[idx][4] < float(0.05)):
            continue
        img0 = cv2.rectangle(
            img0,
            (int(bbox[idx][0]), int(bbox[idx][1])),
            (int(bbox[idx][2]), int(bbox[idx][3])),
            color,
            wt,
        )
        # img0 = cv2.putText(img0, str(idx) + ' ' + names[int(class_id)], (int(bbox[idx][0]), int(bbox[idx][1] + 16)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        # img0 = cv2.putText(img0, '{:.4f}'.format(bbox[idx][4]), (int(bbox[idx][0]), int(bbox[idx][1] + 32)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        # det_result_str += '{} {} {} {} {} {}\n'.format(names[bbox[idx][5]], str(bbox[idx][4]), bbox[idx][0], bbox[idx][1], bbox[idx][2], bbox[idx][3])
    return img0


def letterbox(
    img,
    new_shape=(640, 640),
    color=(114, 114, 114),
    auto=False,
    scaleFill=False,
    scaleup=True,
):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, 64), np.mod(dh, 64)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(
        img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
    )  # add border
    return img, ratio, (dw, dh)


def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None):
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(
            img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1]
        )  # gain  = old / new
        pad = (
            (img1_shape[1] - img0_shape[1] * gain) / 2,
            (img1_shape[0] - img0_shape[0] * gain) / 2,
        )  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    coords[:, [0, 2]] -= pad[0]  # x padding
    coords[:, [1, 3]] -= pad[1]  # y padding
    coords[:, :4] /= gain
    clip_coords(coords, img0_shape)
    return coords


def clip_coords(boxes, shape):
    # Clip bounding xyxy bounding boxes to image shape (height, width)
    if isinstance(boxes, torch.Tensor):  # faster individually
        boxes[:, 0].clamp_(0, shape[1])  # x1
        boxes[:, 1].clamp_(0, shape[0])  # y1
        boxes[:, 2].clamp_(0, shape[1])  # x2
        boxes[:, 3].clamp_(0, shape[0])  # y2
    else:  # np.array (faster grouped)
        boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, shape[1])  # x1, x2
        boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, shape[0])  # y1, y2
