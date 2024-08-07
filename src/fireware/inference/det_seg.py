import cv2
import torch
import numpy as np
import torch.nn.functional as F
from ultralytics.data.augment import LetterBox
import torchvision
import time


def preprocess_letterbox(image):
    letterbox = LetterBox(new_shape=640, stride=32, auto=True)
    image = letterbox(image=image)
    image = (image[..., ::-1] / 255.0).astype(
        np.float32
    )  # BGR to RGB, 0 - 255 to 0.0 - 1.0
    image = image.transpose(2, 0, 1)[None]  # BHWC to BCHW (n, 3, h, w)
    image = torch.from_numpy(image)
    return image


def preprocess_warpAffine(image, dst_width=640, dst_height=640):
    scale = min((dst_width / image.shape[1], dst_height / image.shape[0]))
    ox = (dst_width - scale * image.shape[1]) / 2
    oy = (dst_height - scale * image.shape[0]) / 2
    M = np.array([[scale, 0, ox], [0, scale, oy]], dtype=np.float32)

    img_pre = cv2.warpAffine(
        image,
        M,
        (dst_width, dst_height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(114, 114, 114),
    )
    IM = cv2.invertAffineTransform(M)

    img_pre = (img_pre[..., ::-1] / 255.0).astype(np.float32)
    img_pre = img_pre.transpose(2, 0, 1)[None]
    img_pre = torch.from_numpy(img_pre)
    return img_pre, IM


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


def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y

def non_max_suppression(
        pred, #numpy (1,8400,40(32+2+4))
        conf_thres = 0.25,
        iou_thres = 0.45,
        classes = None, #分类
        agnostic=False,
        multi_label = False,
        labels = (),
        max_det = 300,
        nm = 0, #seg模型 = 32
):
    # 输入是模型推理的结果，即8400个预测框
    # 1,8400,40 [cx,cy,w,h,class*2,32]


    # Checks
    assert 0 <= conf_thres <= 1, f'Invalid Confidence threshold {conf_thres}, valid values are between 0.0 and 1.0'
    assert 0 <= iou_thres <= 1, f'Invalid IoU {iou_thres}, valid values are between 0.0 and 1.0'
    if isinstance(pred, (list, tuple)):  # YOLOv8 model in validation model, output = (inference_out, loss_out)
        pred = pred[0]  # select only inference output

    device = pred.device
    mps = 'mps' in device.type  # Apple MPS
    if mps:  # MPS not fully supported yet, convert tensors to CPU before NMS
        pred = pred.cpu()
    bs = pred.shape[0]  # batch size
    nc = pred.shape[1] - nm - 4  # number of classes
    mi = 4 + nc  # mask start index
    xc = pred[:, 4:mi].amax(1) > conf_thres  # candidates

    # Settings
    max_wh = 7680  # (pixels) maximum box width and height
    max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()
    time_limit = 0.5 + 0.05 * bs  # seconds to quit after
    multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img) 是否为多标签

    t = time.time()

    output = [torch.zeros((0, 6 + nm), device=pred.device)] * bs
    for xi , x in enumerate(pred):
        x = x.transpose(0,-1)[xc[xi]] # 获取符合置信度的框 x = (n,32) 

        #无框
        if not x.shape[0]:
            continue

        # Box/Mask
        box, cls, mask = x.split((4, nc, nm), 1)
        box = xywh2xyxy(box)  # center_x, center_y, width, height) to (x1, y1, x2, y2)
        if multi_label:
            i, j = (cls > conf_thres).nonzero(as_tuple=False).T
            x = torch.cat((box[i], x[i, 4 + j, None], j[:, None].float(), mask[i]), 1)
        else:  # best class only
            conf, j = cls.max(1, keepdim=True)
            x = torch.cat((box, conf, j.float(), mask), 1)[conf.view(-1) > conf_thres]

        # Filter by class
        if classes is not None:
            x = x[(x[:, 5:6] == torch.tensor(classes, device=x.device)).any(1)]

        # Apply finite constraint
        # if not torch.isfinite(x).all():
        #     x = x[torch.isfinite(x).all(1)]

        # Check shape
        n = x.shape[0]  # number of boxes
        if not n:  # no boxes
            continue
        x = x[x[:, 4].argsort(descending=True)[:max_nms]]  # sort by confidence and remove excess boxes

        # Batched NMS
        c = x[:, 5:6] * (0 if agnostic else max_wh)  # classes
        boxes, scores = x[:, :4] + c, x[:, 4]  # boxes (offset by class), scores
        i = torchvision.ops.nms(boxes, scores, iou_thres)  # NMS
        i = i[:max_det]  # limit detections

        output[xi] = x[i]
        if mps:
            output[xi] = output[xi].to(device)

        
    return output


def nmx_v2(pred, conf=0.4, iou=0.5, nm=0):
    return non_max_suppression(pred, conf_thres=conf, iou_thres=iou, nm=nm)


def non_max_suppression_v(
        prediction,
        conf_thres=0.25,
        iou_thres=0.45,
        classes=None,
        agnostic=False,
        multi_label=False,
        labels=(),
        max_det=300,
        nm=0,  # number of masks
):

  # Checks
    assert 0 <= conf_thres <= 1, f'Invalid Confidence threshold {conf_thres}, valid values are between 0.0 and 1.0'
    assert 0 <= iou_thres <= 1, f'Invalid IoU {iou_thres}, valid values are between 0.0 and 1.0'
    if isinstance(prediction, (list, tuple)):  # YOLOv8 model in validation model, output = (inference_out, loss_out)
        prediction = prediction[0]  # select only inference output

    device = prediction.device
    mps = 'mps' in device.type  # Apple MPS
    if mps:  # MPS not fully supported yet, convert tensors to CPU before NMS
        prediction = prediction.cpu()
    bs = prediction.shape[0]  # batch size
    nc = prediction.shape[1] - nm - 4  # number of classes
    mi = 4 + nc  # mask start index
    xc = prediction[:, 4:mi].amax(1) > conf_thres  # candidates

    # Settings
    # min_wh = 2  # (pixels) minimum box width and height
    max_wh = 7680  # (pixels) maximum box width and height
    max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()
    time_limit = 0.5 + 0.05 * bs  # seconds to quit after
    redundant = True  # require redundant detections
    multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)
    merge = False  # use merge-NMS

    t = time.time()
    output = [torch.zeros((0, 6 + nm), device=prediction.device)] * bs
    for xi, x in enumerate(prediction):  # image index, image inference
        # Apply constraints
        # x[((x[:, 2:4] < min_wh) | (x[:, 2:4] > max_wh)).any(1), 4] = 0  # width-height
        x = x.transpose(0, -1)[xc[xi]]  # confidence

        # Cat apriori labels if autolabelling
        if labels and len(labels[xi]):
            lb = labels[xi]
            v = torch.zeros((len(lb), nc + nm + 5), device=x.device)
            v[:, :4] = lb[:, 1:5]  # box
            v[range(len(lb)), lb[:, 0].long() + 4] = 1.0  # cls
            x = torch.cat((x, v), 0)

        # If none remain process next image
        if not x.shape[0]:
            continue

        # Detections matrix nx6 (xyxy, conf, cls)
        box, cls, mask = x.split((4, nc, nm), 1)
        box = xywh2xyxy(box)  # center_x, center_y, width, height) to (x1, y1, x2, y2)
        if multi_label:
            i, j = (cls > conf_thres).nonzero(as_tuple=False).T
            x = torch.cat((box[i], x[i, 4 + j, None], j[:, None].float(), mask[i]), 1)
        else:  # best class only
            conf, j = cls.max(1, keepdim=True)
            x = torch.cat((box, conf, j.float(), mask), 1)[conf.view(-1) > conf_thres]

        # Filter by class
        if classes is not None:
            x = x[(x[:, 5:6] == torch.tensor(classes, device=x.device)).any(1)]

        # Apply finite constraint
        # if not torch.isfinite(x).all():
        #     x = x[torch.isfinite(x).all(1)]

        # Check shape
        n = x.shape[0]  # number of boxes
        if not n:  # no boxes
            continue
        x = x[x[:, 4].argsort(descending=True)[:max_nms]]  # sort by confidence and remove excess boxes

        # Batched NMS
        c = x[:, 5:6] * (0 if agnostic else max_wh)  # classes
        boxes, scores = x[:, :4] + c, x[:, 4]  # boxes (offset by class), scores
        i = torchvision.ops.nms(boxes, scores, iou_thres)  # NMS
        i = i[:max_det]  # limit detections

        output[xi] = x[i]
        if mps:
            output[xi] = output[xi].to(device)

    return output



