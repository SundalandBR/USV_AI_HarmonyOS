import cv2


def display_video(frame_queue):
    print()
    # while True:
    #     frame = frame_queue.get()
    #     if frame is None:  # 结束信号
    #         break
    #     cv2.imshow('Camera', frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # cv2.destroyAllWindows()
    co = 1
    while True:
        a = frame_queue.get()
        # if frame is None:  # 结束信号
        #     break
    #     cv2.imshow('Camera', frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # cv2.destroyAllWindows()
        print(co)
        print(len(a))
        co += 1
        # print(a)
        print("--------------------------")

