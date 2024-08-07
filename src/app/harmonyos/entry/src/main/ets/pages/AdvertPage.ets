import { AdvertClass } from '../utils/ClassUtil';
import { UserSettingClass } from '../utils/setting';
import { window } from '@kit.ArkUI';

@Entry
@Component
struct AdvertPage {
  userSetting: UserSettingClass = new UserSettingClass(getContext(this))
  @State
  adObj: AdvertClass = {
    showAd: false,
    adTime: 0
  }
  timer: number = -1

  closeWin() {
    console.log('跳过')
    window.findWindow("ad_window").destroyWindow()
  }

  async aboutToAppear() {
    this.adObj = await this.userSetting.getUserAd()
    this.timer = setInterval(() => {
      if (this.adObj.adTime === 0) {
        clearInterval(this.timer)
        this.closeWin()
        return
      }
      this.adObj.adTime--
    }, 1000)
  }

  aboutToDisappear(): void {
    clearInterval(this.timer)
  }

  build() {
    Stack({ alignContent: Alignment.TopEnd }) {
      Image(this.adObj.adImg).objectFit(ImageFit.Cover)
      Text(`${this.adObj.adTime}秒后跳过`)
        .padding({ left: 10, right: 10 })
        .margin({ right: 20, top: 30 })
        .height(30)
        .fontSize(14)
        .borderRadius(15)
        .backgroundColor(Color.White)
        .textAlign(TextAlign.Center)
        .onClick(() => {
        this.closeWin()
      })
    }
    .height('100%')
    .width('100%')

  }
}