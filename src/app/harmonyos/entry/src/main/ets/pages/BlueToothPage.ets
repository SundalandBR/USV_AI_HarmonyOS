import { promptAction, router } from '@kit.ArkUI'
import { checkPermissionGrant, requestPermissionsFromUser } from '../utils/Accessutil'
import { common, Permissions } from '@kit.AbilityKit'
import { access, ble } from '@kit.ConnectivityKit'
import { connection } from '@kit.ConnectivityKit';
import { BusinessError } from '@kit.BasicServicesKit'
import { hilog } from '@kit.PerformanceAnalysisKit'

@Entry
@Component
struct BlueToothPage {

  @State Bluestatus:boolean=false
  @State gattClient: ble.GattClientDevice| null = null;
  @State bluetoothname:string[]=[]
  @State matchedbt:string[]=[]
  @State BTMAC:string[]=[]
  PaiBT:string[]=[]
  locationName:string=''
  flag:boolean=false

  // aboutToAppear(): void {
  //   let comtext:common.UIAbilityContext=getContext(this) as common.UIAbilityContext
  //   let permission:Permissions="ohos.permission.ACCESS_BLUETOOTH"
  //
  //   if(!checkPermissionGrant(permission)){
  //     requestPermissionsFromUser(comtext,[permission],'蓝牙')
  //     this.setBluetooth()
  //   }else{
  //     this.setBluetooth()
  //   }
  //
  // }

  //蓝牙状态
  setBluetooth(){
    console.log('获取蓝牙权限成功')
    try {
      let status=access.getState()
      console.log('当前蓝牙状态为：'+status)
      this.Bluestatus=status==access.BluetoothState.STATE_ON
    }catch (err){
      console.log(JSON.stringify(err))
    }

  }


  //开启蓝牙
  onBluetooth(){
    console.log('开启蓝牙');
    try {
      access.enableBluetooth()
    }catch (err){
      console.log(JSON.stringify(err))
    }

  }

  //关闭蓝牙
  offBluetooth(){
    console.log('关闭蓝牙')
    try {
      access.disableBluetooth()
    }catch (err){
      console.log(JSON.stringify(err))
    }
  }

  //获取本机蓝牙名称
  /*getLocationName(){
    console.log('获取本机蓝牙名字')
    let name:string=''
    try {
      name=connection.getLocalName()
    }catch (err){
      console.log(JSON.stringify(err))
    }
    return name
  }*/

  //获取蓝牙列表中各个的蓝牙名字
  onReceiveEvent(data:Array<string>){
    console.log('获取扫描蓝牙列表')
    console.log('列表长度为'+data.length)
    let btName:string=''
    try {
      data.forEach((val:string)=>{
        console.log('蓝牙MAC地址是：'+val)
        this.BTMAC.push(val)
        //this.bluetoothname.push(val)
        //console.log(`${this.bluetoothname}`)
        //console.info(`${this.BTMAC}`)

        btName=connection.getRemoteDeviceName(val)
        console.log('蓝牙名字为：'+btName)
        this.bluetoothname.push(btName)

      })
    }catch (err){
      console.log(JSON.stringify(err)+`${this.bluetoothname}`)
    }

  }

  //发起蓝牙配
  InitiateTeam(sequence:number){
    console.log('发起蓝牙配对:'+sequence)
    let BTmac:string=this.BTMAC[sequence]
    try {
      connection.pairDevice(BTmac,(err:BusinessError)=>{
        console.info('pairDevice, device name err:' + JSON.stringify(err))
        if (err) {
          promptAction.showToast({
            message:"配对失败"
          })
          return
        }
        promptAction.showToast({
          message:"配对成功"
        })
      })
    }catch (err){
      console.error('errCode: ' + (err as BusinessError).code + ', errMessage: ' + (err as BusinessError).message)
    }
  }


  //连接蓝牙
  connectionBT(sequence:number){
    console.log('连接蓝牙')
    //60:56:86:6A:42:F1
    try {
      this.gattClient?.close();
      let deviceName=this.BTMAC[sequence]
      //创建
      // hilog.debug(0,"deviceName",this.deviceName)
      if (deviceName != "") {
        this.gattClient = ble.createGattClientDevice(deviceName);
        //发起连接请求
        this.gattClient.connect();
        promptAction.showToast({
          message:"连接成功"
        })
        setTimeout(()=>{
          this.gattClient?.on("BLEConnectionStateChange",(res:ble.BLEConnectionChangeState)=>{
            hilog.debug(0,"bleStatus",JSON.stringify(res))
          })
        },100)
      }
    }catch (err){
      console.log(JSON.stringify(err))
    }
  }


  //获取已配对列表
  PairingBT(){

    try {
      console.log('获取已配对列表')
      let pairName:string=''
      this.PaiBT=connection.getPairedDevices()
      this.PaiBT.forEach((val:string)=>{
        console.log('已配对蓝牙的MAC地址：'+val)
        pairName=connection.getRemoteDeviceName(val)
        console.log('已配对蓝牙的名字：'+pairName)
        this.matchedbt.push(pairName)
      })

    }catch (err){
      console.error('errCode: ' + (err as BusinessError).code + ', errMessage: ' + (err as BusinessError).message)
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
          Text('蓝牙连接')
        }
        .width('60%')
      }
      .margin({top:30,bottom:30})

      Row(){
        Row(){
          Image($r('app.media.bluetooth'))
            .height(40)
            .margin({right:20})
          Text('蓝牙')
        }
        Row(){
          Toggle({type:ToggleType.Switch,isOn:false})
            .onChange((isOn)=>{
              console.log(''+isOn)
              if(isOn){
                this.onBluetooth()
              }else{
                this.offBluetooth()
              }
            })
        }
        .margin({right:10})
      }
      .borderRadius(10)
      .backgroundColor('rgb(204,255,255)')
      .justifyContent(FlexAlign.SpaceBetween)
      .width('100%')
      .height(70)

      Row(){
        Row(){
          Text('蓝牙名称')
            .margin({left:20})
            .fontSize(20)
        }

        Row(){
          /*Text(this.locationName=this.getLocationName())
            .margin({right:10})*/
          Button(){
            Image($r('app.media.shuaxin'))
              .height(35)
              .margin(5)
          }
          .backgroundColor('rgb(244,244,244)')
          .type(ButtonType.Circle)
          .stateEffect(true)
          .margin({right:20})
          .onClick(()=>this.PairingBT())
        }
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceBetween)
      .margin({top:20,bottom:10})

      //已配对设备
      Column(){
        List(){
          ForEach(this.matchedbt,(val:string,id:number)=>{
            ListItem(){
              Row(){
                Text(val)
                  .fontSize(20)
                  .margin({top:10,bottom:10,left:10})
              }
              .backgroundColor(0xf6f6f6)
              .borderRadius(10)
              .width('90%')
              .margin({top:10,bottom:10,left:15,right:10})
              .onClick(()=>this.connectionBT(id))
            }
          })
        }
      }
      .height('35%')


      //可用设备以及他们的名字
      Column(){
        Row(){
          Row(){
            Text('可用设备')
              .fontSize(20)
          }
          .margin({left:20})
          Row(){
            Button(){
              Image($r('app.media.shuaxin'))
                .height(35)
                .margin(5)
            }
            .backgroundColor('rgb(244,244,244)')
            .type(ButtonType.Circle)
            .stateEffect(true)
            .margin({right:20})
            .onClick(()=>{
              if(this.flag==false){
                try {
                  connection.on('bluetoothDeviceFind',(data)=>this.onReceiveEvent(data))
                  connection.startBluetoothDiscovery()
                  this.flag=true
                } catch (err) {
                  console.log(JSON.stringify(err))
                }
                console.log(''+this.flag)
              }else{
                try {
                  connection.stopBluetoothDiscovery()
                  this.flag=false
                } catch (err) {
                  console.log(JSON.stringify(err))
                }
              }
            })
          }
        }

        .justifyContent(FlexAlign.SpaceBetween)
        .width('100%')
        .margin({top:20})
        Row(){
          List(){
            ForEach(this.bluetoothname,(val:string,id:number)=>{
              ListItem(){
                Row(){
                  Text(val)
                    .fontSize(20)
                    .margin({top:10,bottom:10,left:10})
                }
                .backgroundColor(0xf6f6f6)
                .borderRadius(10)
                .width('90%')
                .margin({top:10,bottom:10,left:15,right:10})
                .onClick(()=>this.InitiateTeam(id))
              }
            })
          }
        }
      }
      .backgroundColor(0xf8f8ff)
      .margin({top:20})
      .height('35%')
      .borderRadius(10)
    }
    .padding({left:20,right:20})
  }
}