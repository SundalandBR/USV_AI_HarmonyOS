## 推理模块

### 后处理API

/recognization/nms.py

```python
def post_processing(onnx_model,img_path,height=640, width=640) --> ret_img, rect
```

@param

- onnx_model：onnx模型文件
- img_path:文件路径
- height：缩放高度
- width：缩放长度

@output

- ret_img：标注后的图片
- rect：缩放标注框坐标(最小x坐标，最小y坐标，最大x坐标，最大y坐标)

eg.

```python
ret_img, rect = post_processing('../../resource/model/onnx/yolov8n.onnx',
                                "D://Module_dataset//coco8//images//val//000000000036.jpg")
```

