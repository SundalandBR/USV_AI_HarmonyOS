import { DividerModifier } from '@ohos.arkui.modifier'
import { router, window } from '@kit.ArkUI'
import { common } from '@kit.AbilityKit'
import { interfaceUser } from '../interfaces/InterfaceUser'
import { GetBlueToothCharacteristic, stopBlueToothCharacteristic, unLock } from '../utils/AccessUtil'
import { ble } from '@kit.ConnectivityKit'

@Entry
@Component
struct Index {
  private flag=false
  private subscribeFlag=false
  @State user1:interfaceUser= {
    userId: 0,
    username: '',
    password: '',
    phoneNumber:0,
    devUuidList: '',
    missionIdList: ''
  };

  aboutToAppear(): void {
    try {
      this.user1=router.getParams() as interfaceUser
    }catch (e){
      console.log("some err exist at aboutToAppear-MainPage")
    }
    let context = getContext(this) as common.UIAbilityContext
    window.getLastWindow(context).then((lastWindow)=> {
      lastWindow.setPreferredOrientation(window.Orientation.PORTRAIT)
    })
  }

  build() {
    //侧边栏
    SideBarContainer(SideBarContainerType.Overlay){
      Column(){
        Row(){
          Image($r('app.media.tx'))
            .height(50)
            .margin(20)
          Text(this.user1.username)
        }
        .margin({top:100})
        .width('100%')
        .onClick(()=>{
          router.pushUrl({
            url:'pages/UserPage',
            params:this.user1
          })
        })
        Line()
          .width('100%')
          .height(1)
          .backgroundColor(Color.Black)
        Column(){

          Row(){
            Row(){
              Image($r('app.media.bluetooth'))
                .height(30)
                .margin({top:10,left:20,right:20})
              Text('蓝牙')
                .margin({top:10})
            }
            Row(){
              Image($r('app.media.enter'))
                .height(20)
                .margin({top:10,right:20})
            }
          }
          .justifyContent(FlexAlign.SpaceBetween)
          .width('100%')
          .onClick(()=>{
            router.pushUrl({
              url:'pages/BlueToothPage'
            })
          })

          Row(){
            Row(){
              Image($r('app.media.fk'))
                .height(30)
                .margin({top:10,left:20,right:20})
              Text('用户反馈')
                .margin({top:10})
            }
            Row(){
              Image($r('app.media.enter'))
                .height(20)
                .margin({top:10,right:20})
            }
          }
          .justifyContent(FlexAlign.SpaceBetween)
          .width('100%')
          .onClick(()=>{
            router.pushUrl({
              url:'pages/FeedBackPage'
            })
          })

          Row(){
            Row(){
              Image($r('app.media.gy'))
                .height(30)
                .margin({top:10,left:20,right:20})
              Text('关于我们')
                .margin({top:10})
            }
            Row(){
              Image($r('app.media.enter'))
                .height(20)
                .margin({top:10,right:20})
            }
          }
          .justifyContent(FlexAlign.SpaceBetween)
          .width('100%')
          .onClick(()=>{
            router.pushUrl({
              url:'pages/AboutPage'
            })
          })
        }
        .margin({top:20,bottom:20})
      }
      .backgroundColor(Color.White)
      //设备
      Column(){
        Line()
          .width('100%')
          .height(1)
          .backgroundColor(Color.Black)
        Row(){
          Row(){
            Image($r('app.media.shoubing'))
              .height(100)
          }
          Row(){
            Toggle({type:ToggleType.Switch,isOn:false})
              .onChange((isOn)=>{
                let device:ble.GattClientDevice=AppStorage.get("gattClient") as ble.GattClientDevice
                console.log('test'+device)
                if(isOn){
                  unLock(device,1)
                }
                else{
                  unLock(device,0)
                }
              })
          }
          .margin({right:10})
          //GetBlueToothCharacteristic(AppStorage.get('gattClient') as ble.GattClientDevice)
          Button('订阅事件')
            .onClick(()=>{
              !this.subscribeFlag?GetBlueToothCharacteristic(AppStorage.get('gattClient') as ble.GattClientDevice):stopBlueToothCharacteristic(AppStorage.get('gattClient') as ble.GattClientDevice)
              this.subscribeFlag=!this.subscribeFlag
            })
        }
        .margin({top:10})
        .width('100%')
        .justifyContent(FlexAlign.SpaceBetween)
        .onClick(()=>{
          if(this.flag){
            router.pushUrl({
              url:'pages/OptionPage',
              params:this.user1
            })
          }
        })
      }
      .alignItems(HorizontalAlign.Start)
      .margin({top:90})

    }
    .padding({left:15,right:15})
    .showSideBar(false)
  }
}