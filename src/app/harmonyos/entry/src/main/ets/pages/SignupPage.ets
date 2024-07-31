import { promptAction, router } from '@kit.ArkUI'
import { Json_msg } from '../interfaces/InterfaceUser';
import { rcp } from '@kit.RemoteCommunicationKit';
import { url } from '@kit.ArkTS';
import { BusinessError } from '@kit.BasicServicesKit';

@Entry
@Component
struct SignupPage {
  @State password: string = ''
  @State username: string = ''
  @State private Acc_sign:string='';  //通过字符串保存,实际上时数字
  @State private phone_number:string='';


  Sigup(){
    let session = rcp.createSession();
    let _url = url.URL.parseURL(`http://47.96.237.24:8080/poi/sign?Acc=${this.Acc_sign}&psw=${this.password}&username=${this.username}&phone=${this.phone_number}`);
    session.post(_url).then((response) => {
      //response为rcp.Response对象,服务器返回的内容
      console.log(JSON.stringify(response));
      let obj=response.toJSON() as Json_msg;//将其解析为Json_msg
      console.log(response.toString());
      console.log("obj.code:"+obj.code)
      console.log("obj.msg:"+obj.msg)
      console.log("obj.Data:"+JSON.stringify(obj.Data))
      if(obj.code==1){

        promptAction.showToast({
          message:"注册成功"
        })
        console.log("注册成功")
        router.replaceUrl({
          url:"pages/LoginPage"
        })
        router.clear()
      }else{
        promptAction.showToast({
          message:"用户已存在"
        })
        console.log("注册失败")
      }
    }).catch((err: BusinessError) => {
      console.error(`err: err code is ${err.code}, err message is ${JSON.stringify(err)}`);
    });
  }
  build() {
    Column() {
      Text("水质检测")
        .fontSize(50)
        .fontWeight(FontWeight.Bold).margin({
        bottom: 60
      })
      Row() {
        Text("账号")
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
      }.width("100%")

      Row() {
        Image($r("app.media.user"))
          .width(30)
        TextInput({
          placeholder: "请输入账号"
        }).width(300).onChange((val: string) => {
          this.Acc_sign = val


        })
      }.margin({
        bottom: 8,
        top: 8
      })
      .width("100%")

      Divider().strokeWidth(4)

      Row() {
        Text("用户名")
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
      }.width("100%")
      .margin({top:8})

      Row() {
        Image($r("app.media.user"))
          .width(30)
        TextInput({
          placeholder: "请输入用户名"
        }).width(300).onChange((val: string) => {
          this.username = val


        })
      }.margin({
        bottom: 8,
        top: 8
      })
      .width("100%")

      Divider().strokeWidth(4)

      Row() {
        Text("密码")
          .fontSize(18)
          .fontWeight(FontWeight.Bold).margin({
          bottom: 8,
          top: 8
        })
      }.width("100%")

      Row() {
        Image($r("app.media.lock")).width(30)

        TextInput({
          placeholder: "请输入密码"
        }).width(300).onChange((val: string) => {
          this.password = val


        }).type(InputType.Password)
      }.width("100%")

      Divider().strokeWidth(4)


      Row() {
        Text("电话号码")
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
      }.width("100%")
      .margin({top:8})

      Row() {
        Image($r("app.media.user"))
          .width(30)
        TextInput({
          placeholder: "请输入电话号码"
        }).width(300).onChange((val: string) => {
          this.phone_number = val


        })
      }.margin({
        bottom: 8,
        top: 8
      })
      .width("100%")

      Divider().strokeWidth(4)

      Button("注册")
        .width("40%")
        .height(50)
        .backgroundColor(Color.Blue)
        .type(ButtonType.Normal)
        .margin(50)
        .onClick(() => {
          this.Sigup()
        })



    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .padding({
      left: 20,
      right: 20
    })
  }
}