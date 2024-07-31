import { router } from '@kit.ArkUI'

@Entry
@Component
struct FeedBackPage {

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
          Text('用户反馈')
        }
        .width('60%')
      }
      .margin({top:30,bottom:30})
      Row(){
        TextArea({placeholder:'请输入反馈信息'})
          .height(200)
      }
      Row(){
        Button('提交').onClick(()=>{
          AlertDialog.show({
            message:'提交成功'
          })
        })
          .width(200)

      }
      .margin({top:30})
    }
    .padding({left:20,right:20})
  }
}