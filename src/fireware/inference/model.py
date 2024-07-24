from nms import post_processing
import letter_box
import numpy as np
import onnxruntime as rt
import cv2
import os
import time


class result:
    def __init__(self,path):
        self.path = path
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Config file not found at {self.path}")
        self.orig_img,self.orig_shape = self.orig()
        self.speed = dict(preprocess = 0,inference = 0,postprocess = 0)
        self.ret_img = self.orig_img
        self.rect = []
        self.probs = []
    
    def orig(self):
        img = cv2.imread(self.path)
        return img,img.shape


class model:
    def __init__(self,model_path,img_path,width = 640,height = 640):
        self.results = result(img_path)
        self.model = model_path
        self.img = self.results.orig_img
        self.width = width
        self.height = height

    def inference(self):
        x_scale = self.img.shape[1] / self.width
        y_scale = self.img.shape[0] / self.height
        start = time.time()
        #img = letter_box.letterbox_image(self.img)
        img = self.img / 255.
        img = cv2.resize(img, (self.width, self.height))
        img = np.transpose(img, (2, 0, 1))
        data = np.expand_dims(img, axis=0)
        end = time.time()
        self.results.speed['preprocess'] = (end - start) * 100 
        start = time.time()
        sess = rt.InferenceSession(self.model)
        input_name = sess.get_inputs()[0].name
        label_name = sess.get_outputs()[0].name
        pred = sess.run([label_name], {input_name: data.astype(np.float32)})[0]
        end = time.time()
        self.results.speed['inference'] = (end - start) * 100
        start = time.time()
        self.results.ret_img,self.results.rect,self.results.probs= post_processing(pred,self.img,x_scale,y_scale)
        end = time.time()
        self.results.speed['postprocess'] = (end - start) * 100
        return self.results


