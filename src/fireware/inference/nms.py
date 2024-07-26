import onnxruntime as rt
import numpy as np
import cv2
import matplotlib.pyplot as plt
import letter_box as lb
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"



def nms(pred, conf_thres, iou_thres):
    """
    非极大值抑制nms
    Args:
        pred: 模型输出特征图
        conf_thres: 置信度阈值
        iou_thres: iou阈值
    Returns: 输出后的结果
    """
    box = pred[pred[..., 4] > conf_thres]  # 置信度筛选
    cls_conf = box[..., 5:]
    cls = []
    for i in range(len(cls_conf)):
        cls.append(int(np.argmax(cls_conf[i])))
 
    total_cls = list(set(cls))  # 记录图像内共出现几种物体
    output_box = []
    # 每个预测类别分开考虑
    for i in range(len(total_cls)):
        clss = total_cls[i]
        cls_box = []
        temp = box[:, :6]
        for j in range(len(cls)):
            # 记录[x,y,w,h,conf(最大类别概率),class]值
            if cls[j] == clss:
                temp[j][5] = clss
                cls_box.append(temp[j][:6])
        #  cls_box 里面是[x,y,w,h,conf(最大类别概率),class]
        cls_box = np.array(cls_box)
        sort_cls_box = sorted(cls_box, key=lambda x: -x[4])  # 将cls_box按置信度从大到小排序
        # box_conf_sort = np.argsort(-box_conf)
        # 得到置信度最大的预测框
        max_conf_box = sort_cls_box[0]
        output_box.append(max_conf_box)
        sort_cls_box = np.delete(sort_cls_box, 0, 0)
        # 对除max_conf_box外其他的框进行非极大值抑制
        while len(sort_cls_box) > 0:
            # 得到当前最大的框
            max_conf_box = output_box[-1]
            del_index = []
            for j in range(len(sort_cls_box)):
                current_box = sort_cls_box[j]
                iou = get_iou(max_conf_box, current_box)
                if iou > iou_thres:
                    # 筛选出与当前最大框Iou大于阈值的框的索引
                    del_index.append(j)
            # 删除这些索引
            sort_cls_box = np.delete(sort_cls_box, del_index, 0)
            if len(sort_cls_box) > 0:
                output_box.append(sort_cls_box[0])
                sort_cls_box = np.delete(sort_cls_box, 0, 0)
    return output_box
 
 
def xywh2xyxy(*box):
    """
    将xywh转换为左上角点和左下角点
    Args:
        box:
    Returns: x1y1x2y2
    """
    ret = [box[0] - box[2] // 2, box[1] - box[3] // 2, \
          box[0] + box[2] // 2, box[1] + box[3] // 2]
    return ret
 
def get_inter(box1, box2):
    """
    计算相交部分面积
    Args:
        box1: 第一个框
        box2: 第二个框
    Returns: 相交部分的面积
    """
    x1, y1, x2, y2 = xywh2xyxy(*box1)
    x3, y3, x4, y4 = xywh2xyxy(*box2)
    # 验证是否存在交集
    if x1 >= x4 or x2 <= x3:
        return 0
    if y1 >= y4 or y2 <= y3:
        return 0
    # 将x1,x2,x3,x4排序，因为已经验证了两个框相交，所以x3-x2就是交集的宽
    x_list = sorted([x1, x2, x3, x4])
    x_inter = x_list[2] - x_list[1]
    # 将y1,y2,y3,y4排序，因为已经验证了两个框相交，所以y3-y2就是交集的宽
    y_list = sorted([y1, y2, y3, y4])
    y_inter = y_list[2] - y_list[1]
    # 计算交集的面积
    inter = x_inter * y_inter
    return inter
 
def get_iou(box1, box2):
    """
    计算交并比： (A n B)/(A + B - A n B)
    Args:
        box1: 第一个框
        box2: 第二个框
    Returns:  # 返回交并比的值
    """
    box1_area = box1[2] * box1[3]  # 计算第一个框的面积
    box2_area = box2[2] * box2[3]  # 计算第二个框的面积
    inter_area = get_inter(box1, box2)
    union = box1_area + box2_area - inter_area   #(A n B)/(A + B - A n B)
    iou = inter_area / union
    return iou


def cod_trf(result, pre, after):
    """
    因为预测框是在经过letterbox后的图像上做预测所以需要将预测框的坐标映射回原图像上
    Args:
        result:  [x,y,w,h,conf(最大类别概率),class]
        pre:    原尺寸图像
        after:  经过letterbox处理后的图像
    Returns: 坐标变换后的结果,
    """
    res = np.array(result)
    x, y, w, h, conf, cls = res.transpose((1, 0))
    x1, y1, x2, y2 = xywh2xyxy(x, y, w, h)  # 左上角点和右下角的点
    h_pre, w_pre, _ = pre.shape
    h_after, w_after, _ = after.shape
    scale = max(w_pre/w_after, h_pre/h_after)  # 缩放比例
    h_pre, w_pre = h_pre/scale, w_pre/scale  # 计算原图在等比例缩放后的尺寸
    x_move, y_move = abs(w_pre-w_after)//2, abs(h_pre-h_after)//2  # 计算平移的量
    ret_x1, ret_x2 = (x1 - x_move) * scale, (x2 - x_move) * scale
    ret_y1, ret_y2 = (y1 - y_move) * scale, (y2 - y_move) * scale
    ret = np.array([ret_x1, ret_y1, ret_x2, ret_y2, conf, cls]).transpose((1, 0))
    return ret


def draw(img, xscale, yscale, pred):
    img_ = img.copy()
    rect = []
    if len(pred):
        for detect in pred:
            detect = [int((detect[0] - detect[2] / 2) * xscale), int((detect[1] - detect[3] / 2) * yscale),
                      int((detect[0] + detect[2] / 2) * xscale), int((detect[1] + detect[3] / 2) * yscale)]
            rect.append(detect)
            img_ = cv2.rectangle(img, (detect[0], detect[1]), (detect[2], detect[3]), (0, 255, 0), 1)
    return img_, rect


def post_processing(pred,conf=0.25,iou=0.45):
    pred = np.squeeze(pred)
    pred = np.transpose(pred, (1, 0))
    pred_class = pred[..., 4:]
    pred_conf = np.max(pred_class, axis=-1)
    pred = np.insert(pred, 4, pred_conf, axis=-1)
    result = nms(pred,conf,iou)
    return result



if __name__ == '__main__':
    height, width = 640, 640
    img0 = cv2.imread('D:\\Module_dataset\\flow_dataset\\images\\train\\000521.jpg')
    x_scale = img0.shape[1] / width
    y_scale = img0.shape[0] / height
    dst_size = (640,640)
    img = lb.letterbox_image(img0,dst_size)
    #img, scale_ratio, pad_size = lb.letterbox_yolo(img0,dst_size)
    imgy = img
    cv2.imwrite('shape.jpg', img)
    img = img / 255.0
    #img = cv2.resize(img, (width, height))
    img = img[:, :, ::-1].transpose(2, 0, 1)
    data = np.expand_dims(img, axis=0)
    sess = rt.InferenceSession('..\\..\\..\\resource\\onnx\\best.onnx')
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    pred = sess.run([label_name], {input_name: data.astype(np.float32)})[0]
    pred = np.squeeze(pred)
    pred = np.transpose(pred, (1, 0))
    pred_class = pred[..., 4:]
    pred_conf = np.max(pred_class, axis=-1)
    pred = np.insert(pred, 4, pred_conf, axis=-1)
    results = nms(pred, 0.25, 0.45)
    print(results)
    results = np.array(results)
    #lb.scale_coords([640, 640], results[:, :4], img0.shape,ratio_pad=(scale_ratio, pad_size))
    img_dw = lb.draw_bbox(results, imgy, (0, 255, 0),2)
    cv2.imwrite('result.png', img_dw)
    # for result in results:
    #     print("rect", result[:4], "truth", result[4], "type", result[5])
    # ret_img, rect = draw(img0, x_scale, y_scale, results)
    # ret_img = ret_img[:, :, ::-1]
    # plt.imshow(ret_img)
    # plt.show()
    # ret_img, rect = post_processing("..\\..\\..\\resource\\onnx\\train15_best.onnx",
    #                                 "D:\\Module_dataset\\flow_dataset\\images\\val\\000002.jpg")
    # print(rect)
    # ret_img = ret_img[:, :, ::-1]
    # plt.imshow(ret_img)
    # plt.show()