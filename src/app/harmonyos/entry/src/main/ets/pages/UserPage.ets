import { router } from '@kit.ArkUI'
import { interfaceUser } from '../interfaces/InterfaceUser'

@Entry
@Component
struct UserPage {

  @State user2:interfaceUser= {
    userId: 0,
    username: '',
    password: '',
    phoneNumber:0,
    devUuidList: '',
    missionIdList: ''
  };

  aboutToAppear(): void {
    try {
      this.user2=router.getParams() as interfaceUser
    }catch (e){
      console.log("some err exist at aboutToAppear-MainPage")
    }
  }

  build() {
    Column(){
      Row(){
        Row(){
          Image($r('app.media.back'))
            .onClick(()=>{
              router.back()
            })
            .height(20)
        }
        .width('40%')
        Row(){
          Text('个人信息')
        }
        .width('60%')
      }
      .margin({top:30,bottom:30})
      Line()
        .width('100%')
        .height(1)
        .backgroundColor(Color.Black)

      Row(){
        Row(){
          Image($r('app.media.tx'))
            .height(70)
            .margin({right:20})
        }
        .width('46%')
        Row(){
          Column(){
            Text(this.user2.username)
              .margin({bottom:5})
            Text('ID：'+this.user2.userId)
          }.alignItems(HorizontalAlign.Start)
        }
      }
      .width('100%')
      .margin({top:20,bottom:20})
      Line()
        .width('100%')
        .height(1)
        .backgroundColor(Color.Black)
      Column(){
        Row(){
          Row(){
            Text('手机号')
          }
          Row(){
            Text(''+this.user2.phoneNumber)
            Image($r('app.media.enter'))
              .height(20)
          }

        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceBetween)
        .margin({top:20})
        Row(){
          Row(){
            Text('密码')
          }
          Row(){
            Text('修改密码')
            Image($r('app.media.enter'))
              .height(20)
          }
        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceBetween)
        .margin({top:20})
        Row(){
          Row(){
            Text('注销账号')
          }
          Row(){
            Text('注销后无法恢复')
            Image($r('app.media.enter'))
              .height(20)
          }

        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceBetween)
        .margin({top:20})

        Row(){
          Button('退出登录')
            .type(ButtonType.Normal)
            .backgroundColor(Color.Red)
            .width(200)
            .onClick(()=>{
              router.replaceUrl({
                url:'pages/LoginPage'
              })
              router.clear()
            })
        }
        .margin({top:30})

      }
    }
    .padding({left:20,right:20})
  }
}