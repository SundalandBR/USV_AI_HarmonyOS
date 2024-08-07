import pyttsx3
import ffmpeg
import os
#
# engine = pyttsx3.init()   # 初始化TTS引擎
# engine.setProperty('voice', 'espeak')  # 设置TTS引擎为espeak


class Voice_Broadcast:
    def __init__(self):
        self.engine = pyttsx3.init()  # 初始化TTS引擎
        self.engine.setProperty("voice", "espeak")
        
        self.engine.setProperty('volume', 100)

    def voice_broadcast(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def startUping_checks(self, flag):
        if flag == 1:
            self.voice_broadcast("无人艇正在关机")
            vb.engine.save_to_file("无人艇正在关机", "startUping_checks.wav")
            vb.engine.runAndWait()

    def water_quality(self, flag):
        if flag == 1:
            self.voice_broadcast("启动水质检测")
            vb.engine.save_to_file("启动水质检测", "water_quality.wav")
            vb.engine.runAndWait()

    def startUp_checks(self, flag):
        if flag:
            # print("无人艇启动成功。")
            self.voice_broadcast("无人艇启动成功开始航行。")
            vb.engine.save_to_file("无人艇启动成功开始航行。", "startUp_checks.wav")
            vb.engine.runAndWait()
        else:
            self.voice_broadcast("无人艇启动失败，请检查。")
            vb.engine.save_to_file(
                "无人艇启动失败，请检查。", "startUp_checks_error.wav"
            )
            vb.engine.runAndWait()
            # print("无人艇启动失败，请检查系统。")

    def shutDown_checks(self, flag):
        if flag:
            self.voice_broadcast("无人艇关机成功。")
            vb.engine.save_to_file("无人艇关机成功。", "shutDown_checks.wav")
            vb.engine.runAndWait()
        else:
            self.voice_broadcast("无人艇关机失败，请检查。")
            vb.engine.save_to_file(
                "无人艇关机失败，请检查。", "shutDown_checks_error.wav"
            )
            vb.engine.runAndWait()

    def shutDowning_checks(self, flag):
        if flag:
            self.voice_broadcast("无人艇正在关机。")
            vb.engine.save_to_file("无人艇正在关机。", "shutDowning_checks.wav")
            vb.engine.runAndWait()

    def voyageTypeChange_check(self, flag):
        if flag:
            self.voice_broadcast("自动导航系统已停止，转为手动控制。")
            vb.engine.save_to_file(
                "自动导航系统已停止，转为手动控制。", "voyageTypeChange_check.wav"
            )
            vb.engine.runAndWait()

    def findObstacle_check(self, flag):
        if flag:
            self.voice_broadcast(
                "前方发现障碍物,自动导航系统已重新规划航线，避开障碍。"
            )
            vb.engine.save_to_file(
                "前方发现障碍物,自动导航系统已重新规划航线，避开障碍。",
                "findObstacle_check.wav",
            )
            vb.engine.runAndWait()

    def returnOriginalRoute(self, flag):
        if flag:
            self.voice_broadcast("障碍物已避开，恢复原定航线。")
            vb.engine.save_to_file(
                "障碍物已避开，恢复原定航线。", "returnOriginalRoute.wav"
            )
            vb.engine.runAndWait()

    def startReturnVoyage_checks(self, flag):
        if flag:
            self.voice_broadcast("无人艇自动返航开始。")
            vb.engine.save_to_file(
                "无人艇自动返航开始。", "startReturnVoyage_checks.wav"
            )
            vb.engine.runAndWait()

    def overReturnVoyage_checks(self, flag):
        if flag:
            self.voice_broadcast("无人艇自动返航结束。")
            vb.engine.save_to_file(
                "无人艇自动返航结束。", "overReturnVoyage_checks.wav"
            )
            vb.engine.runAndWait()


def testos(num):
    instruction = "play "
    path = "sound/"
    wav_file = ""
    if num == 1:
        wav_file = "findObstacle_check.wav"
    elif num == 2:
        wav_file = "overReturnVoyage_checks.wav"
    elif num == 3:
        wav_file = "returnOriginalRoute.wav"
    elif num == 4:
        wav_file = "shutDown_checks_error.wav"
    elif num == 5:
        wav_file = "shutDown_checks.wav"
    elif num == 6:
        wav_file = "shutDowning_checks.wav"
    elif num == 7:
        wav_file = "startReturnVoyage_checks.wav"
    elif num == 8:
        wav_file = "startUp_checks_error.wav"
    elif num == 9:
        wav_file = "startUp_checks.wav"
    elif num == 10:
        wav_file = "startUping_checks.wav"
    elif num == 11:
        wav_file = "voyageTypeChange_check.wav"
    elif num == 12:
        wav_file = "water_quality.wav"

    print(instruction + path + wav_file)
    os.system(instruction + path + wav_file)


if __name__ == "__main__":
    vb = Voice_Broadcast()
    vb.findObstacle_check(1)


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
