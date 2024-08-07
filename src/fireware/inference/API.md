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



### 航控模块API

#### MAVLinkCommunicator 类

\src\fireware\PX4\mavlink_interface.py

`MAVLinkCommunicator` 类负责与无人机飞控系统（如PX4）进行MAVLink通信，实现对无人机的控制和监控。

##### 构造函数
- **`__init__()`**  
  - 功能：初始化日志记录、配置解析器，设置MAVLink通信参数。
  - 参数：无
  - 返回：无

##### 连接方法
- **`connect_to_px4()`**  
  - 功能：根据配置文件中的参数建立与PX4飞控的连接。
  - 参数：无
  - 返回：无

##### 发送控制命令方法
- **`send_move_message_to_px4(action, direction)`**  
  - 功能：向PX4发送移动指令，包括悬停、前进、后退以及转向。
  - 参数：
    - `action` (int): 动作类型（0: 悬停, 1: 前进, 2: 后退）。
    - `direction` (int): 转向方向（0: 左转, 1: 右转）。
  - 返回：无

- **`send_mission_message_to_px4(seq)`**  
  - 功能：向PX4发送任务项到达信号。
  - 参数：
    - `seq` (int): 任务项序列号。
  - 返回：无

- **`send_arm_disarm_command(arm)`**  
  - 功能：发送无人机启动或停止的指令。
  - 参数：
    - `arm` (bool): True为启动，False为停止。
  - 返回：无

##### 数据接收与处理方法
- **`receive_and_parse_messages_from_px4(processor)`**  
  - 功能：接收PX4发送的数据并使用指定的处理器进行处理。
  - 参数：
    - `processor` (DataProcessor对象): 数据处理对象。
  - 返回：无

##### 通信测试与状态检查方法
- **`test_send_capability()`**  
  - 功能：测试与PX4的发送能力。
  - 参数：无
  - 返回：布尔值，表示测试是否成功。

- **`check_heartbeat()`**  
  - 功能：检查是否能接收到PX4的心跳包。
  - 参数：无
  - 返回：布尔值，表示是否接收到心跳。

- **`connect_and_check_communication()`**  
  - 功能：连接并检查与PX4的通信能力。
  - 参数：无
  - 返回：布尔值，表示通信是否正常。

#### DataProcessor 类

\src\fireware\PX4\data_processor.py

`DataProcessor` 类用于处理MAVLink消息，解析无人机的状态和传感器数据。

##### 构造函数
- **`__init__()`**  
  - 功能：初始化用于存储各类消息数据的字典和列表。
  - 参数：无
  - 返回：无

##### 数据处理方法
- **`process_message(msg)`**  
  - 功能：根据MAVLink消息的类型，调用相应的私有方法进行解析。
  - 参数：
    - `msg` (MAVLink消息对象): 接收到的MAVLink消息。
  - 返回：无

##### 解析特定类型消息的方法
- **`_parse_xxx(msg)`** (如`_parse_raw_imu`, `_parse_global_position`等)  
  - 功能：解析特定类型的MAVLink消息，如原始IMU数据、全局位置、飞行姿态等。
  - 参数：
    - `msg` (MAVLink消息对象): 接收到的MAVLink消息。
  - 返回：无

示例代码：
```python
from mavlink_interface import MAVLinkCommunicator
from data_processor import DataProcessor

# 创建MAVLink通信对象
communicator = MAVLinkCommunicator()

# 连接到PX4飞控
communicator.connect_to_px4()

# 创建数据处理对象
processor = DataProcessor()

# 发送移动指令
communicator.send_move_message_to_px4(action=1, direction=0)  # 向前并左转

# 接收并处理数据
communicator.receive_and_parse_messages_from_px4(processor)
```



### 语音播报模块API

#### Voice_Broadcast 类

\src\fireware\PX4\voice_broadcast.py

`Voice_Broadcast` 类提供文本到语音转换的功能，用于实现无人机状态和警告信息的语音播报。

#### 构造函数
- **`__init__()`**  
  - 功能：初始化语音引擎，设置语音属性以支持中文语音播报。
  - 参数：无
  - 返回：无

#### 语音播报方法
- **`voice_broadcast(text)`**  
  - 功能：将提供的文本转换为语音并进行播报。
  - 参数：
    - `text` (str): 需要播报的文本信息。
  - 返回：无

#### 特定状态播报方法
- **`startUping_checks(flag)`**  
  - 功能：播报无人艇关机状态。
  - 参数：
    - `flag` (int): 状态标志，1表示执行播报。
  - 返回：无

- **`water_quality(flag)`**  
  - 功能：播报启动水质检测状态。
  - 参数：
    - `flag` (int): 状态标志，1表示执行播报。
  - 返回：无

- **`startUp_checks(flag)`**  
  - 功能：根据启动状态播报成功或失败信息。
  - 参数：
    - `flag` (bool): True表示启动成功，False表示失败。
  - 返回：无

- **`shutDown_checks(flag)`**  
  - 功能：根据关机状态播报成功或失败信息。
  - 参数：
    - `flag` (bool): True表示关机成功，False表示失败。
  - 返回：无

- **`shutDowning_checks(flag)`**  
  - 功能：播报无人艇正在关机状态。
  - 参数：
    - `flag` (bool): True表示执行播报。
  - 返回：无

- **`voyageTypeChange_check(flag)`**  
  - 功能：播报自动导航系统停止，转为手动控制的状态。
  - 参数：
    - `flag` (bool): True表示执行播报。
  - 返回：无

- **`findObstacle_check(flag)`**  
  - 功能：播报发现障碍物并重新规划航线的信息。
  - 参数：
    - `flag` (bool): True表示执行播报。
  - 返回：无

- **`returnOriginalRoute(flag)`**  
  - 功能：播报障碍物已避开，恢复原定航线的信息。
  - 参数：
    - `flag` (bool): True表示执行播报。
  - 返回：无

- **`startReturnVoyage_checks(flag)`**  
  - 功能：播报无人艇自动返航开始的信息。
  - 参数：
    - `flag` (bool): True表示执行播报。
  - 返回：无

#### 测试方法
- **`testos(num)`**  
  - 功能：测试播放特定编号的语音文件。
  - 参数：
    - `num` (int): 语音文件的编号。
  - 返回：无

示例代码：
```python
from voice_broadcast import Voice_Broadcast

# 创建语音播报对象
vb = Voice_Broadcast()

# 播报无人艇启动成功信息
vb.startUp_checks(True)

# 播报发现障碍物信息
vb.findObstacle_check(True)

# 测试播放编号为10的语音文件
vb.testos(10)
```



### 摄像头模块API

\src\fireware\PX4\capture_video.py

#### 概述
摄像头模块提供了从摄像头捕获视频流、编码图片、保存视频和推流的功能。

#### 函数列表

1. **`capture_camera()`**
2. **`get_folder_size(folder_path)`**
3. **`clear_folder_contents(folder_path)`**
4. **`capture_video(frame_queue, enable)`**
5. **`video_upload(frame_queue, HOST=None, PORT=None)`**

#### 1. 获取摄像头对象
- **`capture_camera()`**  
  - 功能：初始化并打开默认摄像头。
  - 参数：无
  - 返回：cv2.VideoCapture对象或None（如果摄像头无法打开）

#### 2. 计算文件夹大小
- **`get_folder_size(folder_path)`**  
  - 功能：计算指定文件夹的总大小（以字节为单位）。
  - 参数：
    - `folder_path` (str): 目标文件夹的路径。
  - 返回：int，文件夹的总大小（字节）

#### 3. 清空文件夹内容
- **`clear_folder_contents(folder_path)`**  
  - 功能：清空指定文件夹内的所有内容，包括文件和子文件夹。
  - 参数：
    - `folder_path` (str): 目标文件夹的路径。
  - 返回：无

#### 4. 捕获视频并保存
- **`capture_video(frame_queue, enable)`**  
  - 功能：从摄像头捕获视频流，保存为视频文件，并可将图片帧发送到推理模块。
  - 参数：
    - `frame_queue` (queue): 用于存储图片帧的队列。
    - `enable` (threading.Event): 控制线程运行的事件标志。
  - 返回：无

#### 5. 视频推流
- **`video_upload(frame_queue, HOST=None, PORT=None)`**  
  - 功能：将捕获的视频帧编码并通过网络推流到指定服务器。
  - 参数：
    - `frame_queue` (queue): 用于获取待编码和推流的图片帧的队列。
    - `HOST` (str, 可选): 推流服务器的主机名或IP地址，默认从配置文件读取。
    - `PORT` (int, 可选): 推流服务器监听的端口号，默认从配置文件读取。
  - 返回：无

#### 配置文件参数
摄像头模块会读取`config.ini`文件中的`[VIDEO]`部分，以获取推流服务器的`HOST`和`PORT`。

#### 示例代码
```python
import cv2
from queue import Queue
from threading import Event
import capture_video

# 创建队列和事件标志
frame_queue = Queue()
enable = Event()
enable.set()

# 开始捕获视频
capture_video.capture_video(frame_queue, enable)

# 推流（在另一个线程中运行，或根据实际需求调整）
# capture_video.video_upload(frame_queue)
```

