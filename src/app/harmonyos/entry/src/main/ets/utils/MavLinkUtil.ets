import { ble } from '@kit.ConnectivityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { CommandLongT, CreateCommandLongT,
  CreateMissionCountT,
  CreateMissionItemIntT,
  HexToJson, JsonToHex, MissionCountT,
  MissionItemIntT } from '../interfaces/MavLink_Data'
import { BusinessError } from '@kit.BasicServicesKit'
import { mapCommon } from '@kit.MapKit'


let index:number=0;
let pointArr2:mapCommon.LatLng[]=[]
//获取蓝牙特征值并订阅蓝牙事件
function GetBlueToothCharacteristic(gattClient:ble.GattClientDevice){
  let str:string=""
  //解析数据包(mavlink)
  gattClient.getServices()
    .then(res=>{
      res.forEach((item:ble.GattService)=>{
        hilog.debug(0,"service",JSON.stringify(item))
        //采用合适的蓝牙特征值来接收来自MAV的消息
        let characteristicUuid:string = "49535343-1E4D-4BD9-BA61-23C647249616"
        let serviceUuid:string = "49535343-FE7D-4AE5-8FA9-9FAFD205E455"
        let descriptorUuid:string = "00002902-0000-1000-8000-00805F9B34FB"
        if (item.serviceUuid == serviceUuid) {
          console.log('蓝牙服务id:' + item.serviceUuid)
          item.characteristics.forEach((item)=>{
            if (item.characteristicUuid == characteristicUuid){
              let descriptor: ble.BLEDescriptor = {
                serviceUuid: serviceUuid,
                characteristicUuid: characteristicUuid,
                descriptorUuid: descriptorUuid,
                descriptorValue: new ArrayBuffer(8)
              };
              let characteristic:ble.BLECharacteristic = {
                serviceUuid,
                characteristicUuid,
                characteristicValue:new ArrayBuffer(8),
                descriptors:[descriptor]
              }
              gattClient.setCharacteristicChangeIndication(characteristic,true,(err)=>{
                console.log('err:'+JSON.stringify(err))
              });

              gattClient.on('BLECharacteristicChange',(res:ble.BLECharacteristic)=>{
                //返回的二进制特征值（MAV返回的数据包）
                let value = res.characteristicValue;
                // console.log('value'+new Uint8Array(value))
                //判断消息什么什么的 写在这里
                str=HexToJson(value)
                let obj:object=JSON.parse(str)
                let k=JSON.stringify(str,["mav_cmd"])
                // console.log('str:'+str)
                // console.log('mav_cmd:'+k)
                console.log('k:'+k)
                if(obj['mav_cmd']==40){
                  console.log('obj_mav_cmd:'+obj['mav_cmd'])
                }


                let temp:number=obj['mav_cmd']
                switch (temp){
                  case 51:

                  case 40://响应点数量和任务信息
                    console.log('航点信息响应')
                    sendPoint(pointArr2,gattClient,index)
                    console.log('k:'+k)
                    index++;
                    console.log('index:'+index)
                    if(pointArr2.length==index){
                      index=0
                      break;
                    }
                    //AppStorage.setOrCreate('mav_cmd',51)
                    break;
                  case 47:
                    AppStorage.setOrCreate('mav_cmd',47)
                    break;
                  case 147:
                    AppStorage.setOrCreate('mav_cmd',147)//电池状态
                    AppStorage.setOrCreate('BatteryStatus',str)
                    break;
                  case 24:
                    AppStorage.setOrCreate('mav_cmd',24)//GPS
                    AppStorage.setOrCreate('GPS',str)
                    break;
                  case 74:
                    AppStorage.setOrCreate('mav_cmd',74)//HUD
                    break;
                  default :
                    //console.log('什么都没有')
                    break;
                }
              })
            }
          })
        }
      })
    })
}

//上传航点
function sendPoint(marker:mapCommon.LatLng[],gattClient:ble.GattClientDevice,i:number){
  let missionItemInt:MissionItemIntT=CreateMissionItemIntT(0,0,16,0,0,0,0,0,0,marker[i].latitude,marker[i].longitude,0,2)
  let obj_str1=JSON.stringify(missionItemInt)
  createBluetoothCharacteristic(obj_str1,gattClient)
}

//发送指令
function sendCommand(command:number,confirmation:number,param1: number,param2: number,param3: number,param4: number,param5: number,param6: number,param7: number){
  let Navigate:CommandLongT=CreateCommandLongT(command,confirmation,param1,param2,param3,param4,param5,param6,param7)
  let obj_str=JSON.stringify(Navigate)
  let obj_array=JsonToHex(obj_str)
  let arrBuffer=obj_array.buffer
  hilog.info(0x0000, 'testTag', 'obj_array.length = %{public}d', obj_array.length);
  for(let i=0;i<obj_array.length;i++){
    hilog.info(0x0000, 'testTag', 'obj_array[%{public}d] = %{public}d',i,obj_array[i]);
  }
  return arrBuffer
}

//写入蓝牙特征值
function WriteBlueToothCharacteristic(command:number,confirmation:number,param1: number,param2: number,param3: number,param4: number,param5: number,param6: number,param7: number,gattClient:ble.GattClientDevice){
  //let gattClient: ble.GattClientDevice=ble.createGattClientDevice(mac)
  let characteristicUuid:string = "49535343-8841-43F4-A8D4-ECBE34729BB3"
  let serviceUuid:string = "49535343-FE7D-4AE5-8FA9-9FAFD205E455"

  //假设为mavlink消息数据包,用于发送消息指令给飞控
  //const arrayBuffer = new ArrayBuffer(8);

  let arrayBuffer=sendCommand(command,confirmation,param1,param2,param3,param4,param5,param6,param7)

  let characteristic:ble.BLECharacteristic = {
    serviceUuid,
    characteristicUuid,
    characteristicValue:arrayBuffer,
    descriptors:[]
  }

  gattClient.writeCharacteristicValue(characteristic,ble.GattWriteType.WRITE).then(()=>{
    console.log("写入成功")
  }).catch((e:BusinessError)=>{
    console.log('写入失败'+JSON.stringify(e))
  });
}

//解锁和上锁，0：上锁，1：解锁
function unLock(gattClient:ble.GattClientDevice,lock:number){
  let param:CommandLongT=CreateCommandLongT(400,0,lock,21196,0,0,0,0,0)
  let obj_json=JSON.stringify(param)
  console.log('生成的json;' + obj_json)
  // let obj_array=JsonToHex(obj_json)
  // console.log('生成的objArray;' + JSON.stringify(obj_array))
  //console.log('解锁:'+mac)
  //let gattClient: ble.GattClientDevice=ble.createGattClientDevice(mac)
  // let serviceUuid:string = "49535343-FE7D-4AE5-8FA9-9FAFD205E455"
  // let characteristicUuid:string = "49535343-8841-43F4-A8D4-ECBE34729BB3"
  //let descriptorUuid:string = "00002902-0000-1000-8000-00805F9B34FB"
  // let arraybuffer:ArrayBuffer = obj_array.buffer as ArrayBuffer
  // let descriptors: Array<ble.BLEDescriptor> = [];
  // let descriptor: ble.BLEDescriptor = {
  //   serviceUuid: serviceUuid,
  //   characteristicUuid: characteristicUuid,
  //   descriptorUuid: descriptorUuid,
  //   descriptorValue: arraybuffer
  // };
  // descriptors[0] = descriptor;
  //
  // let countMi:ArrayBuffer=obj_array.buffer as ArrayBuffer;
  // console.log("--->" +new Uint8Array(countMi))
  // let characteristic1:ble.BLECharacteristic = {
  //   serviceUuid: serviceUuid,
  //   characteristicUuid: characteristicUuid,
  //   characteristicValue: countMi,
  //   descriptors:[]
  // }
  //
  //
  // gattClient.writeCharacteristicValue(characteristic1,ble.GattWriteType.WRITE)
  //   .then(()=>{
  //     console.log("写入成功")
  //   }).catch((e:BusinessError)=>{
  //   console.log('写入失败'+JSON.stringify(e))
  // })
  createBluetoothCharacteristic(obj_json,gattClient)
}

//创建蓝牙特征值包并发送
function createBluetoothCharacteristic(obj_str:string,gattClient:ble.GattClientDevice){
  let obj_array=JsonToHex(obj_str)
  /*
  hilog.info(0x0000, 'testTag', 'obj_array.length = %{public}d', obj_array.length);
  for(let i=0;i<obj_array.length;i++){
    hilog.info(0x0000, 'testTag', 'obj_array[%{public}d] = %{public}d',i,obj_array[i]);
  }
  * */
  let characteristicUuid:string = "49535343-8841-43F4-A8D4-ECBE34729BB3"
  let serviceUuid:string = "49535343-FE7D-4AE5-8FA9-9FAFD205E455"
  //发送MISSION_COUNT
  let countMi=obj_array.buffer
  let characteristic1:ble.BLECharacteristic = {
    serviceUuid,
    characteristicUuid,
    characteristicValue:countMi,
    descriptors:[]
  }
  gattClient.writeCharacteristicValue(characteristic1,ble.GattWriteType.WRITE)
    .then(()=>{
      console.log("写入成功")
    }).catch((e:BusinessError)=>{
    console.log('写入失败'+JSON.stringify(e))
  });
}

//上传任务
function upload(marker:mapCommon.LatLng[],gattClient:ble.GattClientDevice){
  let count:number=marker.length
  pointArr2=marker;
  let missionCount:MissionCountT=CreateMissionCountT(count,2)
  let obj_str=JSON.stringify(missionCount)
  createBluetoothCharacteristic(obj_str,gattClient)
  /*
  setTimeout(()=>{},1500)

  //循环发送航点MISSION_ITEM_INT
  let i:number=0
  while (count!=0) {
    let cmd=AppStorage.get('mav_cmd') as number
    if(cmd==null){
      continue
    }
    console.log('upload cmd:'+cmd)
    if (cmd == 51) {
      //let obj_t=JSON.parse(str) as MissionRequestIntT
      let missionItemInt: MissionItemIntT =
        CreateMissionItemIntT(0, 0, 16, 0, 0, 0, 0, 0, 0, marker[i].latitude, marker[i].longitude, 0, 2)
      let obj_str1 = JSON.stringify(missionItemInt)
      let obj_array = JsonToHex(obj_str1)
      let arrayBuffer = obj_array.buffer
      i++;
      let characteristic: ble.BLECharacteristic = {
        serviceUuid,
        characteristicUuid,
        characteristicValue: arrayBuffer,
        descriptors: []
      }
      gattClient.writeCharacteristicValue(characteristic, ble.GattWriteType.WRITE).then(()=>{
        console.log("写入航点成功")
      }).catch((e:BusinessError)=>{
        console.log('写入航点失败'+JSON.stringify(e))
      });
      count--;
    }
  }
  //收到最后一个任务的响应
  let cmd=AppStorage.get('mav_cmd') as number
  console.log('upload cmd2:'+cmd)
  let endStr:string=''
  if(cmd==47){
    endStr=AppStorage.get('MISSION_ACK') as string
  }
  let obj_t=JSON.parse(endStr) as MissionAckT
  switch (obj_t.type){
    case 0:
      console.log('任务接受成功');
      promptAction.showToast({
        message:"任务接受成功"
      })
      break
    case 1:
      console.log('    一般错误/现在根本不接受任务命令。');
      promptAction.showToast({
        message:"    一般错误/现在根本不接受任务命令。"
      })
      break
    case 2:
      console.log('不支持坐标系。');
      promptAction.showToast({
        message:"不支持坐标系。"
      })
      break
    case 3:
      console.log(' 不支持命令。');
      promptAction.showToast({
        message:" 不支持命令。"
      })
      break
    case 4:
      console.log('任务物品超出存储空间。');
      promptAction.showToast({
        message:"任务物品超出存储空间。"
      })
      break
    case 5:
      console.log('    其中一个参数的值无效。');
      promptAction.showToast({
        message:"    其中一个参数的值无效。"
      })
      break
    case 6:
      console.log('param1 的值无效。');
      promptAction.showToast({
        message:"param1 的值无效。"
      })
      break
    case 7:
      console.log('    param2 的值无效。');
      promptAction.showToast({
        message:"    param2 的值无效。"
      })
      break
    case 8:
      console.log('    param3 的值无效。');
      promptAction.showToast({
        message:"    param3 的值无效。"
      })
      break
    case 9:
      console.log('    param4 的值无效。');
      promptAction.showToast({
        message:"    param4 的值无效。"
      })
      break
    case 10:
      console.log('    param5 的值无效。');
      promptAction.showToast({
        message:"    param5 的值无效。"
      })
      break
    case 11:
      console.log('    param6 的值无效。');
      promptAction.showToast({
        message:"    param6 的值无效。"
      })
      break
    case 12:
      console.log('    param7 的值无效。');
      promptAction.showToast({
        message:"    param7 的值无效。"
      })
      break
    case 13:
      console.log('接收的任务项目未按顺序排列');
      promptAction.showToast({
        message:"接收的任务项目未按顺序排列"
      })
      break
    case 14:
      console.log('不接受来自此通信伙伴的任何任务命令。');
      promptAction.showToast({
        message:"不接受来自此通信伙伴的任何任务命令。"
      })
      break
    case 15:
      console.log('当前任务操作已取消（例如任务上传、任务下载）。');
      promptAction.showToast({
        message:"当前任务操作已取消（例如任务上传、任务下载）。"
      })
    default :
      console.log('未知错误');
      promptAction.showToast({
        message:"未知错误"
      })
      break
  }
  */
}

//取消订阅
function stopBlueToothCharacteristic(gattClient:ble.GattClientDevice){
  console.log('取消订阅')
  try {
    gattClient.off('BLECharacteristicChange',(res)=>{
      console.log(JSON.stringify(res))
    });
  } catch (err) {
    console.error('errCode: ' + (err as BusinessError).code + ', errMessage: ' + (err as BusinessError).message);
  }
}

//从蓝牙获取状态信息
function getNavigationFromDevice(gattClient:ble.GattClientDevice){
  let navigation=AppStorage.get('') as string
}

export{sendPoint,stopBlueToothCharacteristic,unLock,WriteBlueToothCharacteristic,upload,sendCommand,GetBlueToothCharacteristic}