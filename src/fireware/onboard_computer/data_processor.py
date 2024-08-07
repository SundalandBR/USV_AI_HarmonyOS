import logging
from pymavlink import mavutil
import math
class DataProcessor:
    def __init__(self):
        self.RAW_IMU = dict()
        self.HEARTBEAT = dict()
        self.GLOBAL_POSITION_INT = dict()
        self.VFR_HUD = dict()
        self.ATTITUDE = dict()
        self.SYS_STATUS = dict()
        self.MISSION_ITEM = []
        self.CURRENT_MISSION_ITEM = dict()
        self.MISSION_COUNT = dict()
        self.PARAM_VALUE = dict()
        self.COMMAND_ACK = dict()
        self.COMMAND_LONG = dict()
        self.is_moving = False  # 初始状态为静止
        self.min_speed_threshold = 0.5  # 设定一个最小速度阈值，超过这个值认为艇在移动速
        self.current_mission_item_seq = -1  # 当前执行的航点序号
        self.is_mission_arrival = False #是否到达航点
        self.is_target = False       #是否有目标
        self.is_alive = False       #是否启动
        self.mission_command = None #航点命令


    def process_message(self, msg):
        # 根据消息类型处理消息
        if msg.get_type() == "RAW_IMU":
            self._parse_raw_imu(msg)
        elif msg.get_type() == "GPS_RAW_INT":
            self._parse_global_position(msg)
        elif msg.get_type() == "ATTITUDE":
            self._parse_attitude(msg)
        elif msg.get_type() == "VFR_HUD":
            self._parse_vfr_hud(msg)
        elif msg.get_type() == "SYS_STATUS":
            self._parse_sys_status(msg)
        elif msg.get_type() == "HEARTBEAT":
            self._parse_heartbeat(msg)
        elif msg.get_type() == "MISSION_ITEM":
            self._parse_mission_item(msg)
        elif msg.get_type() == "MISSION_COUNT":
            self._parse_mission_count(msg)
        elif msg.get_type() == "PARAM_VALUE":
            self._parse_param_value(msg)
        elif msg.get_type() == "COMMAND_ACK ":
            self._parse_command_ack(msg)
        elif msg.get_type() == "COMMAND_LONG":
            self._parse_command_long(msg)
        elif msg.get_type() == "MISSION_FINISHED":
            # 处理任务完成消息
            self.handle_mission_finished(msg)


    def _parse_raw_imu(self, msg):
        # 解析原始IMU数据
        accel_x = msg.xacc * 9.81 / 16384  # 将原始数据转换为实际加速度（假设）
        accel_y = msg.yacc * 9.81 / 16384
        accel_z = msg.zacc * 9.81 / 16384
        gyro_x = msg.xgyro * math.pi / 180 / 131
        gyro_y = msg.ygyro * math.pi / 180 / 131
        gyro_z = msg.zgyro * math.pi / 180 / 131

        self.RAW_IMU['type'] = msg.get_type()
        self.RAW_IMU['accel_x'] = accel_x
        self.RAW_IMU['accel_y'] = accel_y
        self.RAW_IMU['accel_z'] = accel_z
        self.RAW_IMU['gyro_x'] = gyro_x
        self.RAW_IMU['gyro_y'] = gyro_y
        self.RAW_IMU['gyro_z'] = gyro_z

    def _parse_global_position(self, msg):
        # 解析全局位置数据

        self.GLOBAL_POSITION_INT['type'] = msg.get_type()
        self.GLOBAL_POSITION_INT['lat'] = msg.lat
        self.GLOBAL_POSITION_INT['lon'] = msg.lon
        self.GLOBAL_POSITION_INT['alt'] = msg.alt
        self.GLOBAL_POSITION_INT['satellites_visible'] = msg.satellites_visible
        # 判断是否到达当前执行的航点以及是否有目标航点
        if self.current_mission_item_seq != -1:
            if abs(self.CURRENT_MISSION_ITEM['x'] - msg.lat) < 0.0001 and abs(self.CURRENT_MISSION_ITEM['y'] - msg.lon) < 0.0001:
                print(f"到达航点 {self.current_mission_item_seq}")
                self.is_mission_arrival = True
                # 到达航点后可以重置当前执行的航点序号
                self.current_mission_item_seq = -1
            else:
                self.is_mission_arrival = False




    def _parse_attitude(self, msg):
        # 解析飞行器姿态
        self.ATTITUDE['type'] = msg.get_type()
        self.ATTITUDE['roll'] = msg.yaw
        self.ATTITUDE['pitch'] = msg.pitch
        self.ATTITUDE['yaw'] = msg.roll

    def _parse_vfr_hud(self, msg):
        # 解析速度、高度和爬升率
        self.VFR_HUD['type'] = msg.get_type()
        self.VFR_HUD['airspeed'] = msg.airspeed
        self.VFR_HUD['groundspeed'] = msg.groundspeed
        self.VFR_HUD['climb'] = msg.climb
        self.VFR_HUD['alt'] = msg.alt
        # 根据地速判断艇的移动状态
        if msg.groundspeed > self.min_speed_threshold and not self.is_moving:
            # 地速超过阈值，且艇之前是静止的，现在认为艇已启动
            self.is_moving = True
            print("艇已启动。")
        elif msg.groundspeed <= self.min_speed_threshold and self.is_moving:
            # 地速低于或等于阈值，且艇之前在移动，现在认为艇已静止
            self.is_moving = False
            print("艇已静止。")

    def _parse_sys_status(self, msg):
        # 解析系统状态信息
        self.SYS_STATUS['type'] = msg.get_type()
        self.SYS_STATUS['onboard_control_sensors_present'] = msg.onboard_control_sensors_present
        self.SYS_STATUS['onboard_control_sensors_enabled'] = msg.onboard_control_sensors_enabled
        self.SYS_STATUS['onboard_control_sensors_health'] = msg.onboard_control_sensors_health
        self.SYS_STATUS['battery_remaining'] = msg.battery_remaining


    def _parse_heartbeat(self, msg):
        # 处理心跳包，通常用于检测连接状态
        is_armed = (msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED) != 0
        self.HEARTBEAT['type'] = msg.get_type()
        self.HEARTBEAT['autopilot'] = msg.autopilot
        self.HEARTBEAT['system_status'] = msg.system_status
        self.HEARTBEAT['mavlink_version'] = msg.mavlink_version
        self.HEARTBEAT['armed'] = is_armed
        # 根据心跳包信息判断无人艇的状态
        # 判断无人艇是否处于启动状态
        if self.HEARTBEAT['system_status'] == mavutil.mavlink.MAV_STATE_ACTIVE and self.HEARTBEAT['armed']:
            self.is_alive = True
        else:
            self.is_alive = False
    #     self.determine_uuv_state()
    #
    # def determine_uuv_state(self):
    #     # 检查开机未解锁状态
    #     if self.HEARTBEAT['system_status'] == mavutil.mavlink.MAV_STATE_BOOT and not self.HEARTBEAT['armed']:
    #         print("无人艇状态: 开机未解锁")
    #
    #     # 检查开机已解锁状态
    #     elif self.HEARTBEAT['system_status'] == mavutil.mavlink.MAV_STATE_CALIBRATED and self.HEARTBEAT['armed']:
    #         print("无人艇状态: 开机已解锁")
    #
    #     # 检查上传任务中状态（这里假设任务上传时系统状态为ACTIVE）
    #     elif self.HEARTBEAT['system_status'] == mavutil.mavlink.MAV_STATE_ACTIVE and not self.HEARTBEAT['armed']:
    #         print("无人艇状态: 上传任务中")
    #
    #     # 检查任务上传成功准备完毕状态（这里假设系统状态为ACTIVE且已解锁）
    #     elif self.HEARTBEAT['system_status'] == mavutil.mavlink.MAV_STATE_ACTIVE and self.HEARTBEAT['armed']:
    #         print("无人艇状态: 任务上传成功准备完毕")
    #
    #     # 检查无人艇启动状态（这里假设系统状态为ACTIVE）
    #     elif self.HEARTBEAT['system_status'] == mavutil.mavlink.MAV_STATE_ACTIVE:
    #         print("无人艇状态: 无人艇启动")
    #
    #     # 其他状态
    #     else:
    #         print("无人艇状态: 其他")

    def _parse_mission_item(self, msg):
        # 解析航点信息
        self.CURRENT_MISSION_ITEM['type'] = msg.get_type()
        self.CURRENT_MISSION_ITEM['seq'] = msg.seq
        self.CURRENT_MISSION_ITEM['frame'] = msg.frame
        self.CURRENT_MISSION_ITEM['command'] = msg.command
        self.CURRENT_MISSION_ITEM['current'] = msg.current
        self.CURRENT_MISSION_ITEM['autocontinue'] = msg.autocontinue
        self.CURRENT_MISSION_ITEM['param1'] = msg.param1
        self.CURRENT_MISSION_ITEM['param2'] = msg.param2
        self.CURRENT_MISSION_ITEM['param3'] = msg.param3
        self.CURRENT_MISSION_ITEM['param4'] = msg.param4
        self.CURRENT_MISSION_ITEM['x'] = msg.x
        self.CURRENT_MISSION_ITEM['y'] = msg.y
        self.CURRENT_MISSION_ITEM['z'] = msg.z
        self.MISSION_ITEM[msg.seq] = self.CURRENT_MISSION_ITEM
        #提取出航点命令
        self.mission_command = msg.command
        # 更新当前执行的航点序号
        if msg.current:
            self.current_mission_item_seq = msg.seq

    def _parse_mission_count(self, msg):
        # 解析任务数量消息
        self.MISSION_COUNT['type'] = msg.get_type()
        self.MISSION_COUNT['count'] = msg.count


    def _parse_param_value(self, msg):
        # 解析参数消息
        self.PARAM_VALUE['type'] = msg.get_type()
        self.PARAM_VALUE['param_id'] = msg.param_id
        self.PARAM_VALUE['param_value'] = msg.param_value
        # 检查是否是电机启动相关的参数
        if msg.param_id == 'MOTOR_START':
            # 假设MOTOR_START参数值为1时表示电机启动
            self.PARAM_VALUE['motor_status'] = bool(msg.param_value == 1)

    def _parse_command_ack(self, msg):
        self.COMMAND_ACK['type'] = msg.get_type()
        self.COMMAND_ACK['command'] = msg.command
        self.COMMAND_ACK['result'] = msg.result

    def _parse_command_long(self, msg):
        # 解析命令长消息
        self.COMMAND_LONG['type'] = msg.get_type()
        self.COMMAND_LONG['command'] = msg.command
        self.COMMAND_LONG['param1'] = msg.param1
        self.COMMAND_LONG['param2'] = msg.param2
        self.COMMAND_LONG['param3'] = msg.param3
        self.COMMAND_LONG['param4'] = msg.param4
        self.COMMAND_LONG['param5'] = msg.param5
        self.COMMAND_LONG['param6'] = msg.param6
        self.COMMAND_LONG['param7'] = msg.param7
        # if msg.command == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM:
        #     if msg.param1:
        #         self.is_alive =  True    #0为解除武装，1为武装(启动)
        #     else:
        #         self.is_alive = False

    def handle_mission_finished(self, msg):
        # 根据任务完成结果执行相应操作
        if msg.mission_result == mavutil.mavlink.MAV_MISSION_ACCEPTED:
            self.is_target = True
            print("所有航点任务成功完成。")
            # 可以在这里添加任务完成后的代码，例如：
            # - 通知用户
            # - 触发数据保存
            # - 发送命令让飞行器返航或着陆
        else:
            self.is_target = False
            print("任务完成状态：", msg.mission_result)
            # 处理任务未成功完成的情况
