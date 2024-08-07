import pyttsx3
from log import logger
import os

#
# engine = pyttsx3.init()   # 初始化TTS引擎
# engine.setProperty('voice', 'espeak')  # 设置TTS引擎为espeak


class Voice_Broadcast:
    def __init__(self):
        self.engine = pyttsx3.init()  # 初始化TTS引擎
        self.engine.setProperty("voice", "zh")
        # self.engine.setProperty('voice', 'zh') #开启支持中文
        # engine.setProperty('voice', voices[0].id)
        # s = self.engine.getProperty('voices')
        voices = self.engine.getProperty("voices")

    def voice_broadcast(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def startUping_checks(self, flag):
        if flag == 1:
            self.voice_broadcast("无人艇正在关机")

    def water_quality(self, flag):
        if flag == 1:
            self.voice_broadcast("启动水质检测")

    def startUp_checks(self, flag):
        if flag:
            # print("无人艇启动成功。")
            self.voice_broadcast("无人艇启动成功开始航行。")
        else:
            self.voice_broadcast("无人艇启动失败，请检查。")
            # print("无人艇启动失败，请检查系统。")

    def shutDown_checks(self, flag):
        if flag:
            self.voice_broadcast("无人艇关机成功。")
        else:
            self.voice_broadcast("无人艇关机失败，请检查。")

    def shutDowning_checks(self, flag):
        if flag:
            self.voice_broadcast("无人艇正在关机。")

    def voyageTypeChange_check(self, flag):
        if flag:
            self.voice_broadcast("自动导航系统已停止，转为手动控制。")

    def findObstacle_check(self, flag):
        if flag:
            self.voice_broadcast(
                "前方发现障碍物,自动导航系统已重新规划航线，避开障碍。"
            )

    def returnOriginalRoute(self, flag):
        if flag:
            self.voice_broadcast("障碍物已避开，恢复原定航线。")

    def startReturnVoyage_checks(self, flag):
        if flag:
            self.voice_broadcast("无人艇自动返航开始。")

    def overReturnVoyage_checks(self, flag):
        if flag:
            self.voice_broadcast("无人艇自动返航开始。")


class sound_enum():
    _FindObstacle = 1       #发现障碍
    _OverReturnVoyage = 2   #返航
    _ShutDown_error = 3     #关机失败
    _ShutDown = 4           #关机成功
    _ShutDowning = 5        #正在关机
    _StartUp_error = 6      #启动失败
    _StartUp = 7            #启动成功
    _WaterQuality = 8       #水质检测

def sound_moudle(_ENABLE, sound_queue):
    while True:
        instruction = "play "
        path = "./sound/"
        if not sound_queue.empty():
            num = sound_queue.get()
            wav_file = ""
            if num == sound_enum._FindObstacle:
                wav_file = "findObstacle_check.wav"
            elif  num == sound_enum._OverReturnVoyage:
                wav_file = "overReturnVoyage_checks.wav"
            elif num == sound_enum._ShutDown_error:
                wav_file = "shutDown_checks_error.wav"
            elif num == sound_enum._ShutDown:
                wav_file = "shutDown_checks.wav"
            elif num == sound_enum._ShutDowning:
                wav_file = "shutDowning_checks.wav"
            elif num == sound_enum._StartUp_error:
                # 无人艇启动失败，请检查。
                wav_file = "startUp_checks_error.wav"
            elif num == sound_enum._StartUp:
                # 无人艇启动成功开始航行。
                wav_file = "startUp_checks.wav"
            elif num == sound_enum._WaterQuality:
                # water_quality
                wav_file = "water_quality.wav"
            try:
                os.system(instruction + path + wav_file)
            except:
                logger.error("no sox device")



# 障碍物警告：
# “注意，前方发现障碍物。”
# “警告，艇体附近有不明物体靠近。”
# 障碍物类型识别：
# “检测到浮标，请小心航行。”
# “注意，前方有渔网，请调整航向。”
# 距离和方位信息：
# “障碍物距离左舷100米，正在接近。”
# “正前方200米处发现障碍物，建议减速。”
# 自动规避措施：
# “正在执行自动规避动作，请保持关注。”
# “自动导航系统已重新规划航线，避开左侧障碍。”
# 人工介入提示：
# “请操作人员注意，可能需要手动介入。”
# “建议操作人员接管控制，以处理紧急情况。”
# 系统状态报告：
# “规避系统启动，当前航速正在降低。”
# “自动导航系统已停止，转为手动控制。”
# 后续指令：
# “请确认新的航向，并执行。”
# “障碍物已避开，恢复原定航线。”
# 安全提醒：
# “请检查艇体是否受损。”
# “如需援助，请立即联系支持团队。”
