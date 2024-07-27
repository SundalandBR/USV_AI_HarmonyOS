import { router } from '@kit.ArkUI'

@Entry
@Component
struct AboutPage {

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
          Text('关于我们')
        }
        .width('60%')
      }
      .margin({top:30,bottom:30})
      Row(){
        Text('回去吧，这里什么也没有')
      }
    }
    .padding({left:20,right:20})
  }
}