import { promptAction, router } from '@kit.ArkUI'
import { checkPermissionGrant, requestPermissionsFromUser } from '../utils/AccessUtil'
import { common, Permissions } from '@kit.AbilityKit'
import { geoLocationManager } from '@kit.LocationKit'
import { rcp } from '@kit.RemoteCommunicationKit';
import { url } from '@kit.ArkTS';
import { interfaceUser, Json_msg } from '../interfaces/InterfaceUser'
import { BusinessError } from '@kit.BasicServicesKit'
import { Users } from '../entity/Users'
import { setToken } from '../utils/MysqlUtil'

//登录
@Entry
@Component
struct LoginPage {
  @State password: string = ''
  @State username: string = ''
  getLocation(){
    let context:common.UIAbilityContext=getContext(this) as common.UIAbilityContext
    let permission:Permissions[]=['ohos.permission.APPROXIMATELY_LOCATION','ohos.permission.LOCATION']
    let noGrant:Permissions[]=[]
    permission.forEach((val:Permissions)=>{
      if(!checkPermissionGrant(val)){
        noGrant.push(val)
      }
    })
    //判断有无授权
    if(noGrant.length){

    }else{
      //获取定位信息
      if(geoLocationManager.isLocationEnabled()){
        console.log('位置服务正常启动')
        geoLocationManager.getCurrentLocation((err,location:geoLocationManager.Location)=>{
          if(err){
            console.error('出错'+JSON.stringify(err))
          }else{
            console.log('获取定位信息：'+`${location.longitude},维度:${location.latitude}`)
            if(geoLocationManager.isGeocoderAvailable()){
              let request:geoLocationManager.ReverseGeoCodeRequest={
                longitude:location.longitude,
                latitude:location.latitude,
                maxItems:5
              }
              geoLocationManager.getAddressesFromLocation(request).then(res=>{
                res.forEach(v=>{
                  console.log(JSON.stringify((v)))
                })
              })
            }else{
              console.error('请先打开网络')
            }
          }
        })
      }else{
        console.error('请先打开位置服务')
      }
    }

  }
  aboutToAppear(): void {
    let context:common.UIAbilityContext=getContext(this) as common.UIAbilityContext
    let permission:Permissions[]=['ohos.permission.APPROXIMATELY_LOCATION','ohos.permission.LOCATION','ohos.permission.ACCESS_BLUETOOTH']
    let noGrant:Permissions[]=[]
    permission.forEach((val:Permissions)=>{
      if(!checkPermissionGrant(val)){
        noGrant.push(val)
      }
    })
    //判断有无授权
    if(noGrant.length){
      for(let i=0;i<noGrant.length;i++) {
        if (noGrant[i] == permission[3]) {
          requestPermissionsFromUser(context, noGrant, '蓝牙')
        }else{
        requestPermissionsFromUser(context,noGrant,'位置')
        }
      }
    }else{
      //获取定位信息
      if(geoLocationManager.isLocationEnabled()){
        console.log('位置服务正常启动')
        geoLocationManager.getCurrentLocation((err,location:geoLocationManager.Location)=>{
          if(err){
            console.error('出错'+JSON.stringify(err))
          }else{
            console.log('获取定位信息：'+`${location.longitude},维度:${location.latitude}`)
            if(geoLocationManager.isGeocoderAvailable()){
              let request:geoLocationManager.ReverseGeoCodeRequest={
                longitude:location.longitude,
                latitude:location.latitude,
                maxItems:5
              }
              geoLocationManager.getAddressesFromLocation(request).then(res=>{
                res.forEach(v=>{
                  console.log(JSON.stringify((v)))
                })
              })
            }else{
              console.error('请先打开网络')
            }
          }
        })
      }else{
        console.error('请先打开位置服务')
      }
    }
  }

  login(){
    let session = rcp.createSession();
    let _url = url.URL.parseURL(`http://47.96.237.24:8080/poi/login?username=${this.username}&password=${this.password}`);
    console.log( _url.toString() )

    session.post(_url).then((response) => {
      //response为rcp.Response对象,服务器返回的内容
      let obj=response.toJSON() as Json_msg;//将其解析为Json_msg  *Json1
      console.log(response.toString());
      console.log("obj.code:"+obj.code)
      console.log("obj.msg:"+obj.msg)
      console.log("obj.Data:"+JSON.stringify(obj.Data))
      if(obj.code==1){
        console.log("登录成功")
        setToken(obj.msg)
        promptAction.showToast({
          message:"登录成功"
        })
        let temp=JSON.stringify(obj.Data,["userId","username","phoneNumber","devUuidList","missionIdList"]);
        let user1=JSON.parse(temp) as interfaceUser;

        router.replaceUrl({//这里为登录成功后的页面路由,replaceUrl:替换原来的页面(原页面会被销毁)
          url:"pages/Index",
          params:user1//穿给新页面的参数
        })

      }else{
        promptAction.showToast({
          message:"密码或账号错误"
        })
        console.log(obj.msg)
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
        Text("立即注册")
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .onClick(()=>{
            router.pushUrl({
              url:'pages/SignupPage'
            })
          })
        Blank()
        Text("忘记密码")
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
      }.width("100%")
      .margin(10)

      Button("登录")
        .width("40%")
        .height(50)
        .backgroundColor(Color.Blue)
        .type(ButtonType.Normal)
        .margin(10)
        .onClick(() => this.login())



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