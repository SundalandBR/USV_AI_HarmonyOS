import sys
import os
import cv2


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


def letterbox_text():
    dst_size = (640, 640)
    image_path = "D:\\Module_dataset\\images\\train\\07.png"
    image = cv2.imread(image_path)
    cv2.imshow('org_image', image)
    dst_image = letterbox_image(image,dst_size)
    cv2.imshow('dst_imgae',dst_image)
    print(dst_image.shape)
    cv2.waitKey()



if __name__ == '__main__':
    cnt = 0
    if 1 == sys.argv.__len__():
        path = os.getcwd()
    else:
        path = sys.argv[1]
    file_list = os.listdir(path)
    for file_name in file_list:
        split_name = os.path.splitext(file_name)
        suffix = split_name[-1]
        if suffix == '.jpg' or '.bmp' == suffix or '.png' == suffix:
            img_path = os.path.join(path, file_name)
            print(img_path)
            dst_img = letterbox_image(img_path, dst_size)
            cv2.imwrite(os.path.join(path,file_name), dst_img)
            cnt += 1
    print("letter image:", {cnt})
