import sys
import os
import cv2
import numpy as np
import torch


dst_size = (640, 640)


def letterbox_image(img, dst_size=(640,640), pad_color=(114, 114, 114)):
    """
    缩放图片，保持长宽比。
    :param image_src:       原图（numpy）
    :param dst_size:        （h，w）
    :param pad_color:       填充颜色，默认是灰色
    :return image_dst:
    """
    image_src = img
    src_h, src_w = image_src.shape[:2]
    dst_h, dst_w = dst_size
    scale = min(dst_h / src_h, dst_w / src_w)
    pad_h, pad_w = int(round(src_h * scale)), int(round(src_w * scale))
    if image_src.shape[0:2] != (pad_w, pad_h):
        image_dst = cv2.resize(image_src, (pad_w, pad_h), interpolation=cv2.INTER_LINEAR)
    else:
        image_dst = image_src
    top = int((dst_h - pad_h) / 2)
    down = int((dst_h - pad_h + 1) / 2)
    left = int((dst_w - pad_w) / 2)
    right = int((dst_w - pad_w + 1) / 2)
    # add border
    image_dst = cv2.copyMakeBorder(image_dst, top, down, left, right, cv2.BORDER_CONSTANT, value=pad_color)
    return image_dst

def letterbox_yolo(img, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleFill=False, scaleup=True):
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
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)

def letterbox_text():
    dst_size = (640, 640)
    image_path = "D:\\Module_dataset\\flow_dataset\\images\\val\\000002.jpg"
    image = cv2.imread(image_path)
    #cv2.imshow('org_image', image)

    dst_image = letterbox_image(image,dst_size)
    #cv2.imshow('dst_imgae',dst_image)
    cv2.imwrite('shape.jpg',dst_image)
    print(dst_image.shape)
    #cv2.waitKey()

def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None):
    print(img1_shape,img0_shape)
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
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


def draw_bbox(bbox, img0, color, wt):
    #det_result_str = ''
    for idx, class_id in enumerate(bbox[:, 5]):
        if float(bbox[idx][4] < float(0.05)):
            continue
        img0 = cv2.rectangle(img0, (int(bbox[idx][0]), int(bbox[idx][1])), (int(bbox[idx][2]), int(bbox[idx][3])), color, wt)
        #img0 = cv2.putText(img0, str(idx) + ' ' + names[int(class_id)], (int(bbox[idx][0]), int(bbox[idx][1] + 16)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        #img0 = cv2.putText(img0, '{:.4f}'.format(bbox[idx][4]), (int(bbox[idx][0]), int(bbox[idx][1] + 32)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        #det_result_str += '{} {} {} {} {} {}\n'.format(names[bbox[idx][5]], str(bbox[idx][4]), bbox[idx][0], bbox[idx][1], bbox[idx][2], bbox[idx][3])
    return img0

def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleFill=False, scaleup=True):
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
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)


if __name__ == '__main__':
    letterbox_text()
    # cnt = 0
    # if 1 == sys.argv.__len__():
    #     path = os.getcwd()
    # else:
    #     path = sys.argv[1]
    # file_list = os.listdir(path)
    # for file_name in file_list:
    #     split_name = os.path.splitext(file_name)
    #     suffix = split_name[-1]
    #     if suffix == '.jpg' or '.bmp' == suffix or '.png' == suffix:
    #         img_path = os.path.join(path, file_name)
    #         print(img_path)
    #         dst_img = letterbox_image(img_path, dst_size)
    #         cv2.imwrite(os.path.join(path,file_name), dst_img)
    #         cnt += 1
    # print("letter image:", {cnt})
    # img_bgr = cv2.imread('D:\\Module_dataset\\flow_dataset\\images\\val\\000002.jpg', cv2.IMREAD_COLOR)  # 读入图片
    # img, scale_ratio, pad_size = letterbox_yolo(img_bgr, new_shape=[640, 640])  # 对图像进行缩放与填充，保持长宽比
    # cv2.imwrite('shape.jpg',img)
