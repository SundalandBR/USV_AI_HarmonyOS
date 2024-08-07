import argparse
import configparser
import logging
import threading

from pymavlink import mavutil
from data_processor import DataProcessor
import os


class MAVLinkCommunicator:
    def __init__(self):
        # 配置日志
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_file = os.path.join(self.log_dir, "main.log")
        self.error_log_file = os.path.join(self.log_dir, "error.log")

        # 配置基本的日志格式
        logging.basicConfig(filename=self.log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # 创建错误日志器并设置格式
        self.error_logger = logging.getLogger('error_logger')
        self.error_handler = logging.FileHandler(self.error_log_file)
        # 设置错误日志的格式，包含时间戳
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.error_handler.setFormatter(formatter)
        self.error_handler.setLevel(logging.ERROR)
        self.error_logger.addHandler(self.error_handler)

        # 创建配置解析器
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        # 从配置文件中获取端口和波特率
        self.port = self.config.get('MAVLINK', 'port')
        self.baudrate = self.config.getint('MAVLINK', 'baudrate')
        self.mav = None

    def connect_to_px4(self):
        try:
            self.mav = mavutil.mavlink_connection(self.port, baud=self.baudrate)
            print('mav ', self.mav)
            logging.info(f"Connected to PX4 on port {self.port} with baudrate {self.baudrate}")
        except Exception as e:
            self.error_logger.error(f"Failed to connect to PX4: {e}")
            raise

    def send_move_message_to_px4(self, action, direction):
        if self.mav is not None:
            try:
                # 目标系统和组件通常对应于 PX4 的自动驾驶仪系统和主控制器
                target_system = 1  # 通常使用 1 表示主系统
                target_component = mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1

                # 根据 action 发送相应的命令
                if action in (0, 1, 2):  # 0: 悬停, 1: 前进, 2: 后退
                    # 使用 MAV_CMD_DO_CHANGE_SPEED 命令来控制速度
                    # 对于悬停，我们可以设置速度为 0
                    speed = 0 if action == 0 else 3  # 假设前进或后退速度为 5m/s
                    self.mav.mav.command_long_send(
                        target_system,
                        target_component,
                        mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED,
                        mavutil.mavlink.MAV_FRAME_GLOBAL,  # 使用全局坐标系
                        0,  # 未使用的参数
                        speed,  # 速度变化量
                        0,  # 未使用的参数
                        0,  # 未使用的参数
                        0,  # 未使用的参数
                        0,  # 未使用的参数
                        0 if action == 0 else 1  # 0 表示减速到停止，1 表示加速到指定速度
                    )
                    logging.info("Action command (%s) sent to PX4", "HOLD" if action == 0 else "MOVE")
                # 根据 direction 发送转向命令
                if direction in (0, 1):  # 0: 左转, 1: 右转
                    # 使用 MAV_CMD_CONDITION_YAW 命令来控制转向
                    yaw_angle = 45  # 固定的转向角为 45 度
                    yaw_speed = 20  # 假设的转向速度（度/秒）
                    self.mav.mav.command_long_send(
                        target_system,
                        target_component,
                        mavutil.mavlink.MAV_CMD_CONDITION_YAW,
                        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,  # 使用全局坐标系，相对高度
                        direction,  # 参数1，根据方向设置不同的值
                        yaw_angle,  # 目标偏航角度
                        yaw_speed,  # 偏航速度
                        1 if direction == 0 else -1,  # 左转或右转
                        0, 0, 0
                    )
                    logging.info("Direction command (%s) sent to PX4", "LEFT" if direction == 0 else "RIGHT")
                # 发送命令后，等待命令确认
                # command_ack1 = self.mav.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)
                # command_ack2 = self.mav.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)
                # if command_ack1:
                #     logging.info("Command %s acknowledged by PX4", command_ack1.command)
                # else:
                #     logging.warning("Command %s not acknowledged by PX4", command_ack2.command)
                # if command_ack2:
                #     logging.info("Command %s acknowledged by PX4", command_ack2.command)
                # else:
                #     logging.warning("Command %s not acknowledged by PX4", command_ack2.command)
            except Exception as e:
                self.error_logger.error(f"Failed to send simple command: {e}")

    def send_mission_message_to_px4(self, seq):
        # 向PX4发送任务项已到达的信号
        try:
            # 创建一个 MAVLink MISSION_ITEM_REACHED 消息
            mission_item_reached = mavutil.mavlink.MISSION_ITEM_REACHED(
                seq=seq,  # 任务项的序列号
                current=True,  # 表示当前任务项
            )

            # 通过 self.mav 发送消息
            self.mav.send(mission_item_reached)
            logging.info(f"Sent mission item reached message for sequence {seq}")
        except Exception as e:
            self.error_logger.error(f"Failed to send mission item reached message: {e}")

        command = 40  # command 40 为任务点任务完成
        result = 0  # 假设命令执行成功
        try:
            # 创建一个 MAVLink COMMAND_ACK 消息
            command_ack = mavutil.mavlink.COMMAND_ACK(
                command=command,  # 命令 ID
                result=result,  # 执行结果
            )

            # 通过 self.mav 发送消息
            self.mav.send(command_ack)
            logging.info(f"Sent command ack message for command {command} with result {result}")
        except Exception as e:
            self.error_logger.error(f"Failed to send command ack message: {e}")

    def receive_and_parse_messages_from_px4(self, processor):
        print(self.mav)
        if self.mav is not None:
            try:
                while True:
                    msg = self.mav.recv_match(blocking=True)
                    # print(f"Received message: {msg}")
                    if msg is not None:
                        processor.process_message(msg)
            except Exception as e:
                self.error_logger.error(f"Error receiving or processing messages: {e}")

    def test_send_capability(self):
        """测试机载电脑是否能够发送消息到 PX4"""
        try:
            # 发送一个简单的命令，例如请求 PX4 报告其版本信息
            self.mav.mav.command_long_send(
                self.mav.target_system,
                self.mav.target_component,
                mavutil.mavlink.MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES,  # 命令ID
                0, 0, 0, 0, 0, 0, 0, 0, 0  # 参数
            )
            logging.info("Test command sent to PX4.")
            return True
        except Exception as e:
            self.error_logger.error(f"Failed to send test command: {e}")
            return False

    def check_heartbeat(self):
        """检查是否能从 PX4 接收心跳包"""
        while True:  # 无限循环直1到接收到心跳
            if self.mav.wait_heartbeat(10) is not None:
                logging.info("Received heartbeat. Communication established.")
                return True
            else:
                logging.info("Continue Waiting for heartbeat from PX4 10s...")

    def connect_and_check_communication(self):
        """连接到 PX4 并检查发送和接收能力"""
        try:
            logging.info("cd connect_and_check_communication")
            self.connect_to_px4()
            logging.info("connect_to_px4")
            if self.check_heartbeat():  # 检查接收心跳的能力
                if self.test_send_capability():  # 检查发送能力
                    logging.info("Send capability test passed. Communication established.")
                    return True
                else:
                    logging.error("Send capability test failed.")
            else:
                logging.error("Heartbeat check failed.")
            return False
        except Exception as e:
            self.error_logger.error(f"An error occurred: {e}")
            return False

    # 预飞行模式,
    def check_preflight_mode(self):
        def request_system_state(self):
            # 发送请求系统状态的MAVLink命令
            self.mav.mav.command_long_send(
                self.mav.target_system,
                self.mav.target_component,
                mavutil.mavlink.MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIES,
                0, 0, 0, 0, 0, 0, 0, 0, 0
            )

        while True:
            # 接收MAVLink消息
            msg = self.mav.recv_match(blocking=True)
            if msg is not None:
                # 检查消息类型是否为STATUSTEXT，这通常用于发送状态信息
                if msg.get_type() == "STATUSTEXT":
                    # 解析消息内容，检查是否包含预飞行相关的文本
                    if "preflight" in msg.text.lower():
                        # 启动所需的模块
                        print("Preflight mode detected. Launching module...")
                        return True
                        # 例如，调用一个方法来启动模块

    # 飞行模式,全部准备完成，即将航行
    def listen_for_flight_mode(self):
        while True:
            # 阻塞式接收MAVLink消息
            msg = self.mav.recv_match(blocking=True)

            if msg is not None:
                # 检查是否为系统状态消息
                if msg.get_type() == 'SYS_STATUS':
                    # 检查传感器和飞控系统是否就绪
                    if (msg.onboard_control_sensors_present &
                        msg.onboard_control_sensors_enabled &
                        msg.onboard_control_sensors_health) == 0xFFFF:
                        # 所有关键传感器和飞控系统均已就绪
                        self.flight_mode = 'READY_TO_FLY'
                        print("All systems go! Ready to fly.")
                        return True
                    else:
                        self.flight_mode = 'CHECK_SYSTEM_STATUS'
                        print("System not ready. Check sensor and control health.")

    def send_arm_disarm_command(self, arm):
        """
        发送启动或停止无人艇的命令。

        :param arm: 布尔值，True 表示启动，False 表示停止。
        """
        target_system = 1  # 通常使用 1 表示主系统
        target_component = mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1  # PX4 的自动驾驶仪组件ID

        if arm:
            # 启动无人艇
            param1 = 1
        else:
            # 停止无人艇
            param1 = 0
        MAV_CMD_COMPONENT_ARM_DISARM = 201
        try:
            self.mav.mav.command_long_send(
                target_system,
                target_component,
                MAV_CMD_COMPONENT_ARM_DISARM,  # 命令ID
                0, 0, 0, 0, 0, 0, 0,  # 其他参数未使用
                param1  # 参数1，1 表示启动，0 表示停止
            )
            logging.info("Arm/Disarm command sent to PX4.")
        except Exception as e:
            self.error_logger.error(f"Failed to send arm/disarm command: {e}")
