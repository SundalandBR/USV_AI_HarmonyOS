from nms import post_processing,cod_trf
import numpy as np
import onnxruntime as rt
import cv2
import os
import time
from letter_box import letterbox,letterbox_yolo,scale_image,scale_coords,draw_bbox
import torch
from det_seg import postprocess,process_mask,random_color,nmx_v2


class result:
    def __init__(self,path):
        self.path = path
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Config file not found at {self.path}")
        self.orig_img,self.orig_shape = self.orig()
        self.speed = dict(preprocess = 0,inference = 0,postprocess = 0)
        self.ret_img = self.orig_img
        self.pred = []
        self.mask = []
    
    def orig(self):
        img = cv2.imread(self.path)
        return img,img.shape
    
    def show_speed(self):
        for i in self.speed:
            val = self.speed[i]
            print(i,"%5f"%val,"ms")

class model:
    def __init__(self,model_path,width = 640,height = 640,DEVICE_ID=0):
        self.model = model_path
        self.width = width
        self.height = height
        self.DEVICE_ID = DEVICE_ID

    def inference(self, img_path):
        self.results = result(img_path)
        self.img = self.results.orig_img
        print(self.img)
        start = time.time()
        img_, scale_ratio, pad_size = letterbox(self.img, new_shape=[640, 640])
        img = img_ / 255.
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, 0).astype(np.float32)
        end = time.time()
        self.results.speed['preprocess'] = (end - start) * 100
        start = time.time()
        sess = rt.InferenceSession(self.model)
        input_name = sess.get_inputs()[0].name
        label_name = sess.get_outputs()[0].name
        pred = sess.run([label_name], {input_name: img.astype(np.float32)})[0]
        end = time.time()
        self.results.speed['inference'] = (end - start) * 100
        self.probs = post_processing(pred)
        self.results.probs = cod_trf(self.probs, self.img, img_)
        for r in self.results.probs:
            image = cv2.rectangle(self.img, (int(r[0]), int(r[1])), (int(r[2]), int(r[3])), (0, 255, 0), 2)
        self.results.ret_img = image[:, :, ::-1]
        end = time.time()
        self.results.speed['postprocess'] = (end - start) * 100
        return self.results
    
    def inference_om(self,img_path):
        self.results = result(img_path)
        self.img = self.results.orig_img

        base.mx_init()  # 初始化 mxVision 资源  # noqa: F821 from mindx.sdk import base
        
        #数据预处理
        start = time.time()
        img_, scale_ratio, pad_size = letterbox(self.img, new_shape=[640, 640])
        #img = letter_box.letterbox_image(self.img)
        img = self.img / 255.
        img = cv2.resize(img, (self.width, self.height))
        cv2.imwrite('reshape.jpg', img * 255)
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0).astype(np.float32)
        img = np.ascontiguousarray(img)
        img = Tensor(img)  # noqa: F821 from mindx.sdk import Tensor
        end = time.time()
        self.results.speed['preprocess'] = (end - start) * 100 
        start = time.time()
        
        #推理
        model = base.model(modelPath=self.model,deviceId=self.DEVICE_ID)  # noqa: F821 from mindx.sdk import base
        pred = model.infer([img])[0]
        pred.to_host()
        pred = np.array(pred)
        end = time.time()
        self.results.speed['inference'] = (end - start) * 100
        start = time.time()
        #推理后处理
        self.probs = post_processing(pred)
        self.results.probs = cod_trf(self.probs, self.img, img_)
        for r in self.results.probs:
            image = cv2.rectangle(self.img, (int(r[0]), int(r[1])), (int(r[2]), int(r[3])), (0, 255, 0), 2)
        self.results.ret_img = image[:, :, ::-1]
        end = time.time()
        self.results.speed['postprocess'] = (end - start) * 100
        print("inference success!")
        return self.results
    
    def inference_seg(self,img_path):
        #初始化
        self.results = result(img_path)
        self.img = self.results.orig_img
        dst_size = (640,640)
        #预处理
        start = time.time()
        img_, scale_ratio, pad_size = letterbox_yolo(self.img, new_shape=[640, 640])
        img = img_ / 255.
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.expand_dims(img, 0)
        self.results.speed['preprocess'] = (time.time() - start) * 100
        
        #推理
        start = time.time()
        sess = rt.InferenceSession(self.model)
        input_name = sess.get_inputs()[0].name
        pred = sess.run(None, {input_name: img.astype(np.float32)})
        self.results.speed['inference'] = (time.time() - start) * 100
        

        start = time.time()
        #output0 = np.array(pred[0]).transpose((0, 2, 1))
        output0 = pred[0]
        output1 = torch.from_numpy(pred[1][0])
        #pred = postprocess(output0)
        pred = nmx_v2(pred=torch.Tensor(output0),nm=32)
        pred = pred[0]
        print(pred.shape)
        self.results.speed["postprocess"] = (time.time() - start) * 1000


        #后处理
        # start = time.time()
        # output0 = np.array(pred[0]).transpose((0,2,1))
        # output1 = torch.from_numpy(pred[1][0])
        # print(output1.shape)
        # pred = postprocess(output0)
        # pred = torch.from_numpy(np.array(pred))

        masks = process_mask(output1, pred[:, 6:], pred[:, :4], dst_size, True)
        masks = scale_image(im1_shape=img_.shape,masks=masks,im0_shape=self.img.shape)
        masks = masks.transpose((2,0,1)).astype(np.uint8)
        for i,mask in enumerate(masks):
            label = int(pred[i][5])
            color = np.array(random_color(label))
            colored_mask = (np.ones((self.img.shape[0],self.img.shape[1],3))*color).astype(np.uint8)
            masked_colored_mask = cv2.bitwise_and(colored_mask,colored_mask,mask=mask)
            mask_indices = mask == 1
            self.img[mask_indices] = (self.img[mask_indices]*0.6 + masked_colored_mask[mask_indices]*0.4).astype(np.uint8)
        scale_coords([640,640],pred[:,:4],self.img.shape)
        img_dw = draw_bbox(pred,self.img,(0,255,0),2)
        self.results.ret_img = img_dw[:,:,::-1]
        self.results.mask = masks
        self.results.pred = pred
        self.results.speed['postprocess'] = (time.time() - start) * 100
        return self.results




