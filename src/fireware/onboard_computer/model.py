import numpy as np
import onnxruntime as rt
import cv2
import os
import time
import torch

from det_utils import (
    postprocess,
    process_mask,
    random_color,
    letterbox_yolo,
    scale_image,
    draw_bbox,
    scale_coords,
    nmx_v2
)


class result:
    def __init__(self, path=None,img = None):
        if path:
            self.path = path
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"Config file not found at {self.path}")
            self.orig_img, self.orig_shape = self.orig()
        else:
            self.orig_img, self.orig_shape = img,img.shape
        self.speed = dict(preprocess=0, inference=0, postprocess=0)
        self.ret_img = self.orig_img

    def orig(self):
        img = cv2.imread(self.path)
        return img, img.shape

    def show_speed(self):
        for i in self.speed:
            val = self.speed[i]
            print(i, "%5f" % val, "ms")


class model:
    def __init__(
        self, model_path, width=640, height=640, DEVICE_ID=0, dst_size=(640, 640), seg = True
    ):
        self.model = model_path
        self.width = width
        self.height = height
        self.DEVICE_ID = DEVICE_ID
        self.dst_size = dst_size
        self.seg = seg

    def inference_seg_om(self, img_path=None,img=None):
        # 初始化
        if not img_path and not img:
            raise FileNotFoundError(f"Not img")
        if img_path:
            self.results = result(path=img_path)
        else:
            self.results = result(img=img)
        self.img = self.results.orig_img
        base.mx_init()  # 初始化 mxVision 资源  # noqa: F821 from mindx.sdk import base

        # 预处理
        start = time.time()
        img_, scale_ratio, pad_size = letterbox_yolo(self.img, new_shape=[640, 640])
        img = img_ / 255.0
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.expand_dims(img, 0).astype(np.float16)
        img = np.ascontiguousarray(img)
        img = Tensor(img)  # noqa: F821 from mindx.sdk import Tensor
        self.results.speed["preprocess"] = (time.time() - start) * 1000

        # 推理
        start = time.time()
        model = base.model(modelPath=self.model, deviceId=self.DEVICE_ID)  # noqa: F821 from mindx.sdk import base
        pred = model.infer([img])
        self.results.speed["inference"] = (time.time() - start) * 1000

        # 后处理
        start = time.time()
        output0 = np.array(pred[0]).transpose((0, 2, 1))
        output1 = torch.from_numpy(pred[1][0])
        pred = postprocess(output0)
        pred = torch.from_numpy(np.array(pred))
        self.results.speed["postprocess"] = (time.time() - start) * 1000
        
        start = time.time()
        if pred.__len__() != 0:
            self.pred = pred.clone()
            self.output1 = output1
            self.mask_img0 = self.img.copy()
            scale_coords([640, 640], pred[:, :4], self.img.shape)
            img_dw = draw_bbox(pred, self.img, (0, 255, 0), 2)
            self.results.ret_img = img_dw[:, :, ::-1]
            
        # 写回结果
        self.results.mask = output1
        self.results.pred = pred
        self.results.speed["result"] = (time.time() - start) * 1000
        return self.results

    def inference_seg(self, img_path=None,img=None):
        # 初始化
        if img_path is None and img is None:
            raise FileNotFoundError(f"Not img")
        if img_path:
            self.results = result(path=img_path)
        else:
            self.results = result(img=img)
        self.img = self.results.orig_img
        # 预处理
        start = time.time()
        self.img_, scale_ratio, pad_size = letterbox_yolo(
            self.img, new_shape=[640, 640]
        )
        img = self.img_ / 255.0
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.expand_dims(img, 0)
        self.results.speed["preprocess"] = (time.time() - start) * 1000

        # 推理
        start = time.time()
        sess = rt.InferenceSession(self.model)
        input_name = sess.get_inputs()[0].name
        pred = sess.run(None, {input_name: img.astype(np.float32)})
        self.results.speed["inference"] = (time.time() - start) * 1000

        # 后处理
        start = time.time()
        #output0 = np.array(pred[0]).transpose((0, 2, 1))
        output0 = pred[0]
        output1 = torch.from_numpy(pred[1][0])
        #pred = postprocess(output0)
        pred = nmx_v2(pred=torch.Tensor(output0),conf=0.25,iou=0.5,nm=32)
        pred = pred[0]
        self.results.speed["postprocess"] = (time.time() - start) * 1000
        
        start = time.time()
        if pred.__len__() != 0:
            self.pred = pred.clone()
            self.output1 = output1
            self.mask_img0 = self.img.copy()
            scale_coords([640, 640], pred[:, :4], self.img.shape)
            img_dw = draw_bbox(pred, self.img, (0, 255, 0), 2)
            self.results.ret_img = img_dw[:, :, ::-1]
        # 掩码处理
        # start = time.time()
        # masks = process_mask(output1, pred[:, 6:], pred[:, :4], dst_size, True)
        # masks = scale_image(im1_shape=self.img_.shape,masks=masks,im0_shape=self.img.shape)
        # masks = masks.transpose((2,0,1)).astype(np.uint8)
        # for i,mask in enumerate(masks):
        #     label = int(pred[i][5])
        #     color = np.array(random_color(label))
        #     colored_mask = (np.ones((self.img.shape[0],self.img.shape[1],3))*color).astype(np.uint8)
        #     masked_colored_mask = cv2.bitwise_and(colored_mask,colored_mask,mask=mask)
        #     mask_indices = mask == 1
        #     self.img[mask_indices] = (self.img[mask_indices]*0.6 + masked_colored_mask[mask_indices]*0.4).astype(np.uint8)
        # self.results.speed['mask'] = (time.time() - start) * 100
        # 写回结果
        self.results.mask = output1
        self.results.pred = pred
        self.results.speed["result"] = (time.time() - start) * 1000
        return self.results

    def mask(self):
        if self.pred.__len__() != 0:
            output1 = self.output1
            pred = self.pred
            dst_size = self.dst_size
            img = self.mask_img0
            masks = process_mask(output1, pred[:, 6:], pred[:, :4], dst_size, True)
            masks = scale_image(
                im1_shape=self.img_.shape, masks=masks, im0_shape=self.img.shape
            )
            masks = masks.transpose((2, 0, 1)).astype(np.uint8)
            for i, mask in enumerate(masks):
                label = int(pred[i][5])
                color = np.array(random_color(label))
                colored_mask = (np.ones((img.shape[0], img.shape[1], 3)) * color).astype(
                    np.uint8
                )
                masked_colored_mask = cv2.bitwise_and(colored_mask, colored_mask, mask=mask)
                mask_indices = mask == 1
                img[mask_indices] = (
                    img[mask_indices] * 0.6 + masked_colored_mask[mask_indices] * 0.4
                ).astype(np.uint8)
            scale_coords([640, 640], pred[:, :4], self.img.shape)
            img_dw = draw_bbox(pred, img, (0, 255, 0), 2)
            self.results.ret_img = img_dw[:, :, ::-1]
        else :
            pred("None target! in mask()")
