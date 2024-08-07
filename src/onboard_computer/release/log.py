import logging
from logging.handlers import TimedRotatingFileHandler, QueueHandler, QueueListener
import sys
import os

# from queue import Queue
from multiprocessing import Queue

log_queue = Queue(-1)
queue_listener = ""


logdir = "logs"
logfile = f"{logdir}/travel.log"
if not os.path.exists(logdir):
    os.makedirs(logdir, exist_ok=True)


def set_formatter():
    """设置日志格式化器"""
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    return logging.Formatter(fmt, datefmt=datefmt)


def set_queue_handler():
    # 不要给QueueHandler重复设置formatter, 会引起重复嵌套
    handler = QueueHandler(log_queue)
    handler.setLevel(logging.DEBUG)
    return handler


def set_stream_handler(formatter: logging.Formatter):
    # 输出到控制台的日志处理器
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    return handler


def set_timed_rotating_file_handler(formatter: logging.Formatter):
    # 输出到文件的日志处理器, 每天生成一个新文件, 最多保留10个文件
    handler = TimedRotatingFileHandler(
        logfile, when="midnight", backupCount=10, encoding="utf-8"
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    return handler


def close_log_queue():
    # 关闭队列监听器
    global queue_listener
    if queue_listener:
        queue_listener.stop()


def get_logger(name: str = "mylogger", level: int = logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = set_formatter()

    stream_handler = set_stream_handler(formatter)
    file_handler = set_timed_rotating_file_handler(formatter)
    queue_handler = set_queue_handler()

    logger.addHandler(queue_handler)

    global queue_listener
    if not queue_listener:
        queue_listener = QueueListener(
            log_queue, stream_handler, file_handler, respect_handler_level=True
        )
        queue_listener.start()

    return logger


logger = get_logger()

if __name__ == "__main__":
    logger.info("test")
    close_log_queue()
