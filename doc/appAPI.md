### 模块：权限管理

#### 1. checkPermissionGrant
描述：检查应用程序是否授予了特定权限。
参数：permission: Permissions：要检查的权限。
返回：Boolean：如果权限被授予，则返回 true，否则返回 false。
#### 2. requestPermissionsFromUser
描述：向用户请求权限并处理结果。如果权限未被授予，弹出一个提示对话框，提示用户前往设置授予权限。
参数：
    context: common.UIAbilityContext：UI能力的上下文。
    permissions: Permissions[]：要请求的权限数组。
    request: string：描述请求权限的字符串。
返回：
    void
#### 3. openPermissionInSystemSettings
描述：打开系统设置页面，让用户手动授予权限。
参数：context: common.UIAbilityContext：UI能力的上下文。
返回：
void
### 依赖
#### 模块：
    @kit.AbilityKit
    @kit.ConnectivityKit
    @kit.MapKit
    @kit.PerformanceAnalysisKit
    @kit.ArkUI
    @kit.ArkTS
    @kit.BasicServicesKit
### 自定义接口：
    MavLink_Data：用于 MavLink 数据的自定义接口。
    函数描述
    checkPermissionGrant
    使用 bundleManager.getBundleInfoForSelfSync 获取捆绑信息。
    使用 abilityAccessCtrl.createAtManager 创建访问令牌管理器。
    使用 atManager.verifyAccessTokenSync 验证权限状态。
    requestPermissionsFromUser
    使用 abilityAccessCtrl.createAtManager 创建访问令牌管理器。
    使用 atManager.requestPermissionsFromUser 请求用户权限。
    如果权限未被授予，显示一个提示对话框。
    在对话框中提供返回或打开系统设置的选项。
    openPermissionInSystemSettings
    构建一个 Want 对象以打开系统设置页面。
    使用 context.startAbility 导航到设置页面。



### 模块：蓝牙管理
#### 1. GetBlueToothCharacteristic
描述：获取蓝牙特征值并订阅蓝牙事件。
参数：
    gattClient: ble.GattClientDevice：Gatt 客户端设备。
返回：
    void
#### 2. sendPoint
描述：上传航点信息。
参数：
    marker: mapCommon.LatLng[]：航点的经纬度数组。
    gattClient: ble.GattClientDevice：Gatt 客户端设备。
    i: number：航点的索引。
返回：
    void
#### 3. sendCommand
描述：发送指令到设备。
参数：
    command: number：指令代码。
    confirmation: number：确认代码。
    param1: number：参数1。
    param2: number：参数2。
    param3: number：参数3。
    param4: number：参数4。
    param5: number：参数5。
    param6: number：参数6。
    param7: number：参数7。
返回：
    rrayBuffer：指令的二进制数据。
#### 4. WriteBlueToothCharacteristic
描述：写入蓝牙特征值。
参数：
    command: number：指令代码。
    confirmation: number：确认代码。
    param1: number：参数1。
    param2: number：参数2。
    param3: number：参数3。
    param4: number：参数4。
    param5: number：参数5。
    param6: number：参数6。
    param7: number：参数7。
    gattClient: ble.GattClientDevice：Gatt 客户端设备。
返回：
    void
#### 5. unLock
描述：解锁或上锁设备。
参数：
    gattClient: ble.GattClientDevice：Gatt 客户端设备。
    lock: number：锁定状态（0：上锁，1：解锁）。
返回：
    void
#### 6. createBluetoothCharacteristic
描述：创建蓝牙特征值包并发送。
参数：
    obj_str: string：要发送的 JSON 字符串。
    gattClient: ble.GattClientDevice：Gatt 客户端设备。
返回：
    void
#### 7. upload
描述：上传任务。
参数：
    marker: mapCommon.LatLng[]：航点的经纬度数组。
    gattClient: ble.GattClientDevice：Gatt 客户端设备。
返回：
    void
#### 8. stopBlueToothCharacteristic
描述：取消订阅蓝牙特征值事件。
参数：
    gattClient: ble.GattClientDevice：Gatt 客户端设备。
返回：
    void
#### 9. getNavigationFromDevice
描述：从蓝牙设备获取导航状态信息。
参数：
    gattClient: ble.GattClientDevice：Gatt 客户端设备。
返回：
    void
### 依赖
模块：
    @kit.ConnectivityKit
    @kit.PerformanceAnalysisKit
    @kit.BasicServicesKit
    @kit.MapKit
### 自定义接口：
    CommandLongT
    CreateCommandLongT
    CreateMissionCountT
    CreateMissionItemIntT
    HexToJson
    JsonToHex
    MissionCountT
    MissionItemIntT

### 模块：sass连接
#### 变量描述
    全局变量
    IPAddress
    类型: string
    描述: 服务器的IP地址
    默认值: 47.96.237.24
    Port
    类型: number
    描述: 服务器的端口号
    默认值: 8080
    Token_AAA
    类型: string
    描述: 授权令牌，用于身份验证
    默认值: abc
    枚举类型
    TABLE_
    表示数据库表的枚举类型：
    mission_data: 任务数据
    navigation_data: 导航数据
    user_accounts: 用户账户数据
    video_data: 视频数据
    water_quality_data: 水质数据
### 数据类型
#### Json_msg
    描述: 接口返回消息的格式。
    字段:
    code: 响应码，number 类型。
    msg: 响应消息，string 类型。
    Data: 响应数据，string 类型。
    Point
    描述: 表示地理位置的数据类型。
    字段:
    latitude: 纬度，string 类型。
    longitude: 经度，string 类型。
    WaterData
    描述: 表示水质数据的数据类型。
    字段:
    waterDataId: 水质数据ID，number 类型。
    missionId: 任务ID，number 类型。
    timestamp: 时间戳，string 类型。
    latitude: 纬度，number 类型。
    longitude: 经度，number 类型。
    ph: pH值，number 类型。
    dissolvedOxygen: 溶解氧，number 类型。
    conductivity: 电导率，number 类型。
    temperature: 温度，number 类型。
    turbidity: 浊度，number 类型。
    ammoniaNitrogen: 氨氮，number 类型。
    organicMatter: 有机物，number 类型。
#### Mission
    描述: 表示任务数据的数据类型。
    字段:
    missionId: 任务ID，number 类型。
    userId: 用户ID，number 类型。
    createTime: 创建时间，string 类型。
    finishTime: 完成时间，string 类型。
    positionList: 位置列表，string 类型。
    status: 任务状态，number 类型。
    priority: 优先级，number 类型。
    waterDataIdList: 水质数据ID列表，string 类型。
    navigationIdList: 导航ID列表，string 类型。
    description: 描述，string 类型。
    videoId: 视频ID，number 类型。
#### Navigation
    描述: 表示导航数据的数据类型。
    字段:
    navigationId: 导航ID，number 类型。
    missionId: 任务ID，number 类型。
    timestamp: 时间戳，string 类型。
    latitude: 纬度，number 类型。
    longitude: 经度，number 类型。
    speed: 速度，number 类型。
    course: 航向，number 类型。
    status: 状态，number 类型。
    batteryLevel: 电池电量，number 类型。
### 接口函数
#### setToken
    描述: 设置授权令牌。
    参数:
    Token: 授权令牌，string 类型。
#### LoginOut
    描述: 执行登出操作。
    参数:
    callback: 回调函数，参数类型为 boolean，表示登出是否成功。
#### TAdd
    描述: 向指定表添加数据。
    参数:
    tableIndex: 表的索引，类型为 TABLE_ 枚举。
    param1 至 param12: 数据参数，类型均为 string，用于添加的具体数据。
#### TDelete
    描述: 从指定表删除数据。
    参数:
    table: 表的索引，类型为 TABLE_ 枚举。
    id: 数据的ID，类型为 number。
#### TGet
    描述: 获取指定表中的数据。
    参数:
    TableIndex: 表的索引，类型为 TABLE_ 枚举。
    column: 列名，类型为 string。
    value: 列的值，类型为 string。
#### TEdit
    描述: 编辑指定表中的数据。
    参数:
    tableIndex: 表的索引，类型为 TABLE_ 枚举。
    Id: 数据的ID，类型为 number。
    column: 列名，类型为 string。
    value: 列的新值，类型为 string。
#### GetResponseForNavigation
    描述: 获取导航数据。
    参数:
    callback: 回调函数，参数类型为 string，表示导航数据的响应内容。