### 推理模块API

eg.

调用`model.inference`将返回`results`对象

```python
import model
models = model.model("..\\..\\..\\resource\\onnx\\train15_best.onnx",
                                    "D:\\Module_dataset\\flow_dataset\\images\\val\\000002.jpg")
results = models.inference()
```

`results`对象参数

| 参数         | 类型            | 说明                                                       |
| ------------ | --------------- | ---------------------------------------------------------- |
| `path`       | `str`           | 原图片的路径                                               |
| `orig_img`   | `numpy.ndarray` | 原图片                                                     |
| `orig_shape` | `tuple`         | 原图片大小                                                 |
| `speed`      | `dict`          | 预处理、推理、后处理速度                                   |
| `rect`       | `list`          | 缩放标注框坐标(最小x坐标，最小y坐标，最大x坐标，最大y坐标) |
| `probs`      | `list`          | 置信框坐标、置信框、识别的类别                             |

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

