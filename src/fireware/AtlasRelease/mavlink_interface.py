import configparser
import logging

from pymavlink import mavutil
from data_processor import DataProcessor
import time
import os

class MAVLinkCommunicator:
    def __init__(self):
        # 配置日志
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_file = os.path.join(self.log_dir, "main.log")
        self.error_log_file = os.path.join(self.log_dir, "error.log")

        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.error_logger = logging.getLogger('error_logger')
        self.error_handler = logging.FileHandler(self.error_log_file)
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
            logging.info(f"Connected to PX4 on port {self.port} with baudrate {self.baudrate}")
        except Exception as e:
            self.error_logger.error(f"Failed to connect to PX4: {e}")
            raise

    def send_messages_to_px4(self, action, direction):
        if self.mav is not None:
            try:
                # 目标系统和组件通常对应于 PX4 的自动驾驶仪系统和主控制器
                target_system = 1  # 通常使用 1 表示主系统
                target_component = mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1

                # 根据 action 发送相应的命令
                if action in (0, 1, 2):  # 0: 悬停, 1: 前进, 2: 后退
                    # 使用 MAV_CMD_DO_CHANGE_SPEED 命令来控制速度
                    # 对于悬停，我们可以设置速度为 0
                    speed = 0 if action == 0 else 5  # 假设前进或后退速度为 5m/s
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
                    print("Direction command (%s) sent to PX4", "LEFT" if direction == 0 else "RIGHT","success")

            except Exception as e:
                print("Failed to send simple command: {e}")
                self.error_logger.error(f"Failed to send simple command: {e}")

    def receive_and_parse_messages_from_px4(self, processor):
        if self.mav is not None:
            try:
                while True:
                    msg = self.mav.recv_match(blocking=True)
                    if msg is not None:
                        processor.process_message(msg)
            except Exception as e:
                self.error_logger.error(f"Error receiving or processing messages: {e}")

    def run_mavlink(self, processor):
        try:
            while True:
                self.receive_and_parse_messages_from_px4(processor)
                time.sleep(0.01)  # 适当的延时，避免 CPU 占用过高
        except KeyboardInterrupt:
            logging.info("MAVLink communication terminated by user")
        except Exception as e:
            self.error_logger.error(f"Error in MAVLink communication: {e}")

    def test_send_capability(self):
        """测试机载电脑是否能够发送消息到 PX4"""
        try:
            # 发送一个简单的命令，例如请求 PX4 报告其版本信息
            self.mav.mav.command_ack_send(
                mavutil.mavlink.MAV_COMP_ID_AUTOPILOT1,  # 目标组件ID
                mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,  # 命令ID
                mavutil.mavlink.MAV_RESULT_ACCEPTED,  # 假设命令被接受
                0, 0, 0, 0, 0, 0, 0, 0, 0  # 参数
            )
            logging.info("Test command sent to PX4.")
            return True
        except Exception as e:
            self.error_logger.error(f"Failed to send test command: {e}")
            return False

    # def check_heartbeat(self):
    #     """检查是否能从 PX4 接收心跳包"""
    #     while True:  # 无限循环直到接收到心跳
    #         msg = self.mav.recv_match(blocking=True)
    #         if msg is not None and msg.get_type() == "HEARTBEAT":
    #             # 检查心跳是否来自 PX4
    #             if msg.get_srcSystem() == mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER:
    #                 logging.info("Received heartbeat from PX4. Communication established.")
    #                 return True
    #             else:
    #                 logging.warning("Received heartbeat from an unexpected source. Expected PX4.")
    #         else:
    #             logging.info("Waiting for heartbeat from PX4...")
    def check_heartbeat(self):
        """检查是否能从 PX4 接收心跳包"""
        while True:  # 无限循环直到接收到心跳
            if self.mav.wait_heartbeat(10) is not None :
                logging.info("Received heartbeat. Communication established.")
            else:
                logging.info("Continue Waiting for heartbeat from PX4 10s...")
    def connect_and_check_communication(self):
        """连接到 PX4 并检查发送和接收能力"""
        try:
            self.connect_to_px4()
            if self.check_heartbeat():  # 检查接收心跳的能力
                logging.info("Heartbeat received from PX4. Proceeding to send capability test.")
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



if __name__ == "__main__":
    processor = DataProcessor()
    communicator = MAVLinkCommunicator()
    if communicator.connect_and_check_communication():
        communicator.run_mavlink(processor)
    else:
        logging.error("Exiting the program because communication with PX4 could not be established.")