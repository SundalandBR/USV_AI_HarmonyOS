import multiprocessing as mp
import os
from capture_video import capture_video
from display_video import display_video

if __name__ == "__main__":
    os.environ['QT_QPA_PLATFORM'] = 'xcb'

    frame_queue = mp.Queue(maxsize=1)

    capture_process = mp.Process(target=capture_video, args=(frame_queue,))
    display_process = mp.Process(target=display_video, args=(frame_queue,))

    capture_process.start()
    display_process.start()

    print(capture_process.pid)
    print(display_process.pid)

    capture_process.join()
    display_process.join()
