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
        self.MISSION_ITEM = dict()
        self.MISSION_COUNT = dict()
        self.PARAM_VALUE = dict()





    def process_message(self, msg):
        # 根据消息类型处理消息
        if msg.get_type() == "RAW_IMU":
            self._parse_raw_imu(msg)
        elif msg.get_type() == "GLOBAL_POSITION_INT":
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


    def _parse_raw_imu(self, msg):
        # 解析原始IMU数据
        accel_x = msg.xacc * 9.81 / 16384  # 将原始数据转换为实际加速度（假设）
        accel_y = msg.yacc * 9.81 / 16384
        accel_z = msg.zacc * 9.81 / 16384
        gyro_x = msg.xgyro * math.pi / 180 / 131
        gyro_y = msg.ygyro * math.pi / 180 / 131
        gyro_z = msg.zgyro * math.pi / 180 / 131

        self.RAW_IMU['type'] = msg.type
        self.RAW_IMU['accel_x'] = accel_x
        self.RAW_IMU['accel_y'] = accel_y
        self.RAW_IMU['accel_z'] = accel_z
        self.RAW_IMU['gyro_x'] = gyro_x
        self.RAW_IMU['gyro_y'] = gyro_y
        self.RAW_IMU['gyro_z'] = gyro_z

    def _parse_global_position(self, msg):
        # 解析全局位置数据

        self.GLOBAL_POSITION_INT['type'] = msg.type
        self.GLOBAL_POSITION_INT['lat'] = msg.lat
        self.GLOBAL_POSITION_INT['lon'] = msg.lon
        self.GLOBAL_POSITION_INT['alt'] = msg.alt
        self.GLOBAL_POSITION_INT['relative_alt'] = msg.relative_alt


    def _parse_attitude(self, msg):
        # 解析飞行器姿态
        self.ATTITUDE['roll'] = msg.yaw
        self.ATTITUDE['pitch'] = msg.pitch
        self.ATTITUDE['yaw'] = msg.roll
        self.ATTITUDE['type'] = msg.type

    def _parse_vfr_hud(self, msg):
        # 解析速度、高度和爬升率
        self.VFR_HUD['type'] = msg.type
        self.VFR_HUD['airspeed'] = msg.airspeed
        self.VFR_HUD['groundspeed'] = msg.groundspeed
        self.VFR_HUD['climb'] = msg.climb
        self.VFR_HUD['alt'] = msg.alt

    def _parse_sys_status(self, msg):
        # 解析系统状态信息
        self.SYS_STATUS['type'] = msg.type
        self.SYS_STATUS['onboard_control_sensors_present'] = msg.onboard_control_sensors_present
        self.SYS_STATUS['onboard_control_sensors_enabled'] = msg.onboard_control_sensors_enabled
        self.SYS_STATUS['onboard_control_sensors_health'] = msg.onboard_control_sensors_health
        self.SYS_STATUS['battery_remaining'] = msg.battery_remaining


    def _parse_heartbeat(self, msg):
        # 处理心跳包，通常用于检测连接状态
        is_armed = (msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED) != 0
        self.HEARTBEAT['type'] = msg.type
        self.HEARTBEAT['autopilot'] = msg.autopilot
        self.HEARTBEAT['system_status'] = msg.system_status
        self.HEARTBEAT['mavlink_version'] = msg.mavlink_version
        self.HEARTBEAT['armed'] = is_armed

    def _parse_mission_item(self, msg):
        # 解析航点信息
        self.MISSION_ITEM['seq'] = msg.seq
        self.MISSION_ITEM['frame'] = msg.frame
        self.MISSION_ITEM['command'] = msg.command
        self.MISSION_ITEM['current'] = msg.current
        self.MISSION_ITEM['autocontinue'] = msg.autocontinue
        self.MISSION_ITEM['param1'] = msg.param1
        self.MISSION_ITEM['param2'] = msg.param2
        self.MISSION_ITEM['param3'] = msg.param3
        self.MISSION_ITEM['param4'] = msg.param4
        self.MISSION_ITEM['x'] = msg.x
        self.MISSION_ITEM['y'] = msg.y
        self.MISSION_ITEM['z'] = msg.z
        self.MISSION_ITEM['type'] = msg.type
        self.MISSION_ITEM['seq'] = msg.seq

    def _parse_mission_count(self, msg):
        # 解析任务数量消息
        self.MISSION_COUNT['type'] = msg.type
        self.MISSION_COUNT['count'] = msg.count


    def _parse_param_value(self, msg):
        # 解析参数消息
        self.PARAM_VALUE['type'] = msg.type
        self.PARAM_VALUE['param_id'] = msg.param_id
        self.PARAM_VALUE['param_value'] = msg.param_value