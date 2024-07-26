from nms import post_processing,cod_trf
import numpy as np
import onnxruntime as rt
import cv2
import os
import time
from letter_box import letterbox

class result:
    def __init__(self,path):
        self.path = path
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Config file not found at {self.path}")
        self.orig_img,self.orig_shape = self.orig()
        self.speed = dict(preprocess = 0,inference = 0,postprocess = 0)
        self.ret_img = self.orig_img
        self.probs = []
    
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
        start = time.time()
        img_, scale_ratio, pad_size = letterbox(self.img, new_shape=[640, 640])
        img = img_ / 255.
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, 0).astype(np.float32)
        end = time.time()
        self.results.speed['preprocess'] = (end - start) * 100
        start = time.time()
        sess = rt.InferenceSession('..\\..\\..\\resource\\onnx\\best.onnx')
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


