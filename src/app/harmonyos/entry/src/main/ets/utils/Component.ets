import { MapComponent, mapCommon, map } from '@kit.MapKit';
import { BusinessError } from '@kit.BasicServicesKit';
import http from '@ohos.net.http';
import { Map } from '../pages/Map';

@Component
struct componentA {
  aboutToAppear(): void {
    // 感知组件显隐
    console.log('A组件显示');
  }

  aboutToDisappear(): void {
    // 感知组件显隐
    console.log('A组件隐藏');
  }

  build() {
    Column({ space: 10 }) {
      Text('PH:').fontColor(Color.Black).fontWeight(600)
      Text('含氧量:').fontColor(Color.Black).fontWeight(600)
    }
    .alignItems(HorizontalAlign.Start)
    .offset({ x: '70%', y: '5%' })
    .backgroundColor(Color.White)
    .opacity(0.5)
    .width('30%')
    .height('15%')
  }
}

@Component
struct componentB {
  build() {
    Column({ space: 10 }) {
      Video({ src: $r('app.media.sp') }).width('100%').height('100%')
    }
    .alignItems(HorizontalAlign.Start)
    .offset({ x: '70%', y: '25%' })
    .backgroundColor(Color.Black)
    .opacity(0.5)
    .width('30%')
    .height('35%')
  }
}

@Component
struct componentC {
  build() {
    Row({ space: 10 }) {
      Column() {
        Text('0.00').fontColor(Color.Black).fontWeight(600).fontSize(25)
        Text('时速(km/h)').fontColor(Color.Black).fontWeight(600).fontSize(20)
      }

      Row({ space: 5 }) {
        Text('电量:').fontColor(Color.Black).fontWeight(600).fontSize(20)
        Text('70%').fontColor(Color.Black).fontWeight(600).fontSize(20)
      }
    }
    .justifyContent(FlexAlign.SpaceBetween)
    .offset({ x: '40%', y: '80%' })
    .backgroundColor(Color.White)
    .opacity(0.5)
    .width('23%')
    .height('15%')
  }
}

class Mission {
  id: number
  name: string

  constructor(id: number, name: string) {
    this.id = id;
    this.name = name;
  }
}

class Marker {
  id: number
  longitude: number
  latitude: number

  constructor(id: number, longitude: number, latitude: number) {
    this.id = id;
    this.longitude = longitude;
    this.latitude = latitude;
  }
}

class MarkerDialog {
  index: number
  longitude: number
  latitude: number

  constructor(id: number, longitude: number, latitude: number) {
    this.index = id;
    this.longitude = longitude;
    this.latitude = latitude;
  }
}

// let markerDialog: MarkerDialog = new MarkerDialog(0, 0, 0)

@Component
struct componentD {
  @State private missionList: Mission[] = []
  @State private markerList: Marker[] = []
  @State private severIP: string = ''
  @State private markerArr: map.Marker[] = []
  @State private currentMission: number = 0
  @State isShowMarkerComponent: boolean = false;
  @State private markerDialog: MarkerDialog = new MarkerDialog(0, 0, 0)
  @State private mapController: map.MapComponentController = new map.MapComponentController();

  aboutToAppear(): void {
    this.mapController.on("markerDragStart", (marker) => this.markerDragHandler(marker))
    this.mapController.on("mapClick", (position) => this.mapClickHandler(position))
    this.mapController.on("markerClick", (marker) => this.markerClickHandler(marker));
  }

  markerDragHandler(marker: map.Marker) {
    let index = this.markerArr.indexOf(marker)
    console.log('Drag_index:'+index)
    let currentMarker = this.markerList[index]
    console.log('DragMarker_id:'+currentMarker.id)
    this.deleteMarkerRequest(currentMarker.id)
    /*this.markerArr.splice(index,1)
    marker.remove()*/
  }

  markerClickHandler(marker: map.Marker) {
    // console.log("length:"+this.markerArr.length)
    // this.isShowMarkerComponent = false
    console.log('on markerClickHandler');
    let index = this.markerArr.indexOf(marker)
    let currentMarker = this.markerList[index]
    // this.isShowMarkerComponent = true
    // marker.onClick(()=>{})
    this.markerDialog = new MarkerDialog(index + 1, currentMarker.longitude, currentMarker.latitude)
    console.log("markerDialog:"+JSON.stringify(this.markerDialog))
  }

  mapClickHandler(position: mapCommon.LatLng) {
    //this.clickToAddMarker(position)
    if (this.currentMission != 0) {
      this.addMarkerRequest(position)
    }
  }

  @State textValue: string = ''
  @State inputValue: string = 'click me'
  @State list_id: number = 1

  dialogController: CustomDialogController | null = new CustomDialogController({
    builder: CustomDialogExample({
      cancel: ()=> { this.onCancel() },
      confirm: ()=> { this.onAccept() },
      textValue: $textValue,
      inputValue: $inputValue,
      list_id: $list_id,
      severIP: $severIP,
      missionList: $missionList
    }),
    cancel: this.exitApp,
    autoCancel: true,
    onWillDismiss:(dismissDialogAction: DismissDialogAction)=> {
      console.info("reason=" + JSON.stringify(dismissDialogAction.reason))
      console.log("dialog onWillDismiss")
      if (dismissDialogAction.reason == DismissReason.PRESS_BACK) {
        dismissDialogAction.dismiss()
      }
      if (dismissDialogAction.reason == DismissReason.TOUCH_OUTSIDE) {
        dismissDialogAction.dismiss()
      }
    },
    alignment: DialogAlignment.Center,
    // offset: { dx: 0, dy: -20 },
    // gridCount: 4,
    customStyle: false,
    cornerRadius: 10,
  })

  // 在自定义组件即将析构销毁时将dialogController置空
  aboutToDisappear() {
    this.dialogController = null // 将dialogController置空
  }

  onCancel() {
    console.info('Callback when the first button is clicked')
  }

  onAccept() {
    console.info('Callback when the second button is clicked')
  }

  exitApp() {
    console.info('Click the callback in the blank area')
  }

  build() {
    Stack() {
      Column() {
        Column() {
          ForEach(this.missionList, (val: Mission, index: number) => {
            Row({ space: 5 }) {
              Text(val.name).fontColor(Color.Black).fontWeight(600)
            }.justifyContent(FlexAlign.SpaceBetween).onClick(() => {
              //console.log('点击项Index:'+index)
              console.log('点击项ID:' + val.id)
              this.loadMarkerList(val.id)
              this.currentMission = val.id
            })
          })
          /*Row({ space: 5 }) {
            Text('任务1').fontColor(Color.Black).fontWeight(600)
          }.justifyContent(FlexAlign.SpaceBetween)

          Row({ space: 5 }) {
            Text('任务2').fontColor(Color.Black).fontWeight(600)
          }.justifyContent(FlexAlign.SpaceBetween)*/
        }

        Button("+新增任务")
          .width('60%')
          .height('20%')
          .fontColor(Color.Black)
          .fontWeight(600)
          .onClick(() => {
            if (this.dialogController != null) {
              this.dialogController.open()
            }
          })
      }
      .justifyContent(FlexAlign.SpaceBetween)
      .offset({ x: '12%', y: '25%' })
      .backgroundColor(Color.White)
      .opacity(0.5)
      .width('20%')
      .height('30%')
      /*if (this.isShowMarkerComponent) {
        componentMarker({markerDialog:this.markerDialog})
      }*/
      // componentMarker({markerDialog:this.markerDialog})
      // componentMarker({markerDialog})
      // 一开始组件就都有避免动态加载导致布局混乱的同时，让数据传递更方便
      Column({ space: 10 }) {
        Text(`标记${this.markerDialog.index}`).fontColor(Color.Black).fontWeight(600)
        Text(`纬度：${this.markerDialog.latitude}`).fontColor(Color.Black).fontWeight(600)
        Text(`经度：${this.markerDialog.longitude}`).fontColor(Color.Black).fontWeight(600)
      }
      .alignItems(HorizontalAlign.Start)
      .offset({ x: '70%', y: '65%' })
      .backgroundColor(Color.White)
      .opacity(0.5)
      .width('20%')
      .height('20%')
    }
  }

  async addMarkers() {
    for (let i = 0; i < this.markerList.length; i++) {
      let markerOption: mapCommon.MarkerOptions = {
        position: { longitude: this.markerList[i].longitude, latitude: this.markerList[i].latitude },
        draggable: true,
        clickable: true
      }
      //addMarker是异步方法，所以要await它，等它一个个按顺序搞好
      let marker: map.Marker = await this.mapController.addMarker(markerOption);
      console.log('添加标记：' + JSON.stringify(marker.getPosition()))
      this.markerArr.push(marker);

      //将最后一个标记的详细信息显示出来
      let index = this.markerList.length - 1
      let currentMarker = this.markerList[index]
      this.markerDialog = new MarkerDialog(this.markerList.length, currentMarker.longitude, currentMarker.latitude)
    }
  }

  clickToAddMarker(position: mapCommon.LatLng) {
    //在点击位置创建一个点 标记图片显示不全是模拟器的问题
    let markerOption: mapCommon.MarkerOptions = {
      position: position,
      draggable: true,
      clickable: true
    }
    this.mapController.addMarker(markerOption).then(res => {
      console.log('添加标记：' + JSON.stringify(res.getPosition()))
      //this.markerArr.push(res)
      if (this.currentMission != 0) {
        this.addMarkerRequest(res.getPosition())
      }
    }).catch((err: BusinessError) => {
      console.error('标记失败' + JSON.stringify(err))
    })
  }

  loadMarkerList(mission_id: number) {
    let httpRequest = http.createHttp();
    httpRequest.request(
      // 填当前分配的IP地址，不要填localhost或127.0.0.1
      `http://${this.severIP}/getMarkerList/${mission_id}`, //?username=admin&password=123
      {
        method: http.RequestMethod.GET,
        header: {
          "Content-Type": "text/html;charset=UTF-8"
        },
        expectDataType: http.HttpDataType.OBJECT, // 可选，指定返回数据的类型
        usingCache: true, // 可选，默认为true
        priority: 1, // 可选，默认为1
        connectTimeout: 60000, // 可选，默认为60000ms
        readTimeout: 60000, // 可选，默认为60000ms
        usingProtocol: http.HttpProtocol.HTTP1_1, // 可选，协议类型默认值由系统自动指定
      }, (err, data) => {
      if (!err) {
        console.info('Result:' + JSON.stringify(data.result));
        //console.log(JSON.stringify(Object.entries(data.result)))
        let markers: object[] = Object.values(data.result)
        //每次列表更新前重新初始化
        this.markerList = []
        this.markerArr = []
        for (let index = 0; index < markers.length; index++) {
          const element = markers[index];
          console.log('marker_id:' + element['marker_id'])
          console.log('longitude:' + element['longitude'])
          console.log('latitude:' + element['latitude'])
          this.markerList.push(new Marker(element['marker_id'], element['longitude'], element['latitude']))
        }
        console.info('MarkerList:' + JSON.stringify(this.markerList));
        //移除地图上所有的圆、标记、折线等覆盖物
        this.mapController.clear();
        //原来放在onClick下，可能会因为是异步操作，导致执行顺序有误
        this.addMarkers()
      } else {
        console.info('error:' + JSON.stringify(err));
        // 取消订阅HTTP响应头事件
        httpRequest.off('headersReceive');
        // 当该请求使用完毕时，调用destroy方法主动销毁
        httpRequest.destroy();
      }
    }
    );
  }

  addMarkerRequest(position: mapCommon.LatLng) {
    let httpRequest = http.createHttp();
    httpRequest.request(
      // 填当前分配的IP地址，不要填localhost或127.0.0.1
      `http://${this.severIP}/addMarker`, //?username=admin&password=123
      {
        method: http.RequestMethod.POST,
        header: {
          "Content-Type": "application/json"
        },
        extraData: {
          "latitude": position.latitude,
          "longitude": position.longitude,
          "mission_id": this.currentMission
        },
        expectDataType: http.HttpDataType.OBJECT, // 可选，指定返回数据的类型
        usingCache: true, // 可选，默认为true
        priority: 1, // 可选，默认为1
        connectTimeout: 60000, // 可选，默认为60000ms
        readTimeout: 60000, // 可选，默认为60000ms
        usingProtocol: http.HttpProtocol.HTTP1_1, // 可选，协议类型默认值由系统自动指定
      }, (err, data) => {
      if (!err) {
        //添加后重新加载
        this.loadMarkerList(this.currentMission)
      } else {
        console.info('error:' + JSON.stringify(err));
        // 取消订阅HTTP响应头事件
        httpRequest.off('headersReceive');
        // 当该请求使用完毕时，调用destroy方法主动销毁
        httpRequest.destroy();
      }
    }
    );
  }

  deleteMarkerRequest(marker_id: number) {
    let httpRequest = http.createHttp();
    httpRequest.request(
      // 填当前分配的IP地址，不要填localhost或127.0.0.1
      `http://${this.severIP}/deleteMarker`, //?username=admin&password=123
      {
        method: http.RequestMethod.POST,
        header: {
          "Content-Type": "application/json"
        },
        extraData: {
          "mission_id": this.currentMission,
          "marker_id": marker_id
        },
        expectDataType: http.HttpDataType.OBJECT, // 可选，指定返回数据的类型
        usingCache: true, // 可选，默认为true
        priority: 1, // 可选，默认为1
        connectTimeout: 60000, // 可选，默认为60000ms
        readTimeout: 60000, // 可选，默认为60000ms
        usingProtocol: http.HttpProtocol.HTTP1_1, // 可选，协议类型默认值由系统自动指定
      }, (err, data) => {
      if (!err) {
        //添加后重新加载
        this.loadMarkerList(this.currentMission)
      } else {
        console.info('error:' + JSON.stringify(err));
        // 取消订阅HTTP响应头事件
        httpRequest.off('headersReceive');
        // 当该请求使用完毕时，调用destroy方法主动销毁
        httpRequest.destroy();
      }
    }
    );
  }
}

@Component
struct componentMarker {
  @State private markerDialog: MarkerDialog = new MarkerDialog(0, 0, 0)

  build() {
    Column({ space: 10 }) {
      Text(`标记${this.markerDialog.index}`).fontColor(Color.Black).fontWeight(600)
      Text(`纬度：${this.markerDialog.latitude}`).fontColor(Color.Black).fontWeight(600)
      Text(`经度：${this.markerDialog.longitude}`).fontColor(Color.Black).fontWeight(600)
    }
    .alignItems(HorizontalAlign.Start)
    .offset({ x: '80%', y: '65%' })
    .backgroundColor(Color.White)
    .opacity(0.5)
    .width('30%')
    .height('15%')
  }
}

@CustomDialog
@Component
struct CustomDialogExample {
  @Link textValue: string
  @Link inputValue: string
  @Link list_id: number
  @Link severIP:string
  @Link missionList: Mission[]

  controller?: CustomDialogController
  // 若尝试在CustomDialog中传入多个其他的Controller，以实现在CustomDialog中打开另一个或另一些CustomDialog，那么此处需要将指向自己的controller放在所有controller的后面
  cancel: () => void = () => {
  }
  confirm: () => void = () => {
  }

  build() {
    Column() {
      Text('请输入任务名').fontSize(20).margin({ top: 10, bottom: 10 })
      TextInput({ placeholder: '', text: this.textValue }).height(40).width('90%')
        .onChange((value: string) => {
          this.textValue = value
        })
      Flex({ justifyContent: FlexAlign.SpaceAround }) {
        Button('cancel')
          .onClick(() => {
            if (this.controller != undefined) {
              this.controller.close()
              this.cancel()
            }
          }).backgroundColor(0xffffff).fontColor(Color.Black)
        Button('confirm')
          .onClick(() => {
            if (this.controller != undefined) {
              this.inputValue = this.textValue
              this.controller.close()
              this.addMissionRequest()
              //this.confirm()

            }
          }).backgroundColor(0xffffff).fontColor(Color.Red)
      }.margin({ bottom: 10 })

    }.borderRadius(10)
    // 如果需要使用border属性或cornerRadius属性，请和borderRadius属性一起使用。
  }

  addMissionRequest() {
    let httpRequest = http.createHttp();
    httpRequest.request(
      // 填当前分配的IP地址，不要填localhost或127.0.0.1
      `http://${this.severIP}/addMission`, //?username=admin&password=123
      {
        method: http.RequestMethod.POST,
        header: {
          "Content-Type": "application/json"
        },
        extraData: {
          "list_id": this.list_id,
          "name": this.textValue
        },
        expectDataType: http.HttpDataType.OBJECT, // 可选，指定返回数据的类型
        usingCache: true, // 可选，默认为true
        priority: 1, // 可选，默认为1
        connectTimeout: 60000, // 可选，默认为60000ms
        readTimeout: 60000, // 可选，默认为60000ms
        usingProtocol: http.HttpProtocol.HTTP1_1, // 可选，协议类型默认值由系统自动指定
      }, (err, data) => {
      if (!err) {
        //添加后重新加载
        this.loadMissionList()
      } else {
        console.info('error:' + JSON.stringify(err));
        // 取消订阅HTTP响应头事件
        httpRequest.off('headersReceive');
        // 当该请求使用完毕时，调用destroy方法主动销毁
        httpRequest.destroy();
      }
    }
    );
  }

  loadMissionList() {
    let httpRequest = http.createHttp();
    httpRequest.request(
      // 填当前分配的IP地址，不要填localhost或127.0.0.1
      `http://${this.severIP}/getMissionList/${this.list_id}`, //?username=admin&password=123
      {
        method: http.RequestMethod.GET,
        header: {
          "Content-Type": "text/html;charset=UTF-8"
        },
        expectDataType: http.HttpDataType.OBJECT, // 可选，指定返回数据的类型
        usingCache: true, // 可选，默认为true
        priority: 1, // 可选，默认为1
        connectTimeout: 60000, // 可选，默认为60000ms
        readTimeout: 60000, // 可选，默认为60000ms
        usingProtocol: http.HttpProtocol.HTTP1_1, // 可选，协议类型默认值由系统自动指定
      }, (err, data) => {
      if (!err) {
        this.missionList = []
        console.info('Result:' + JSON.stringify(data.result));
        //console.log(JSON.stringify(Object.entries(data.result)))
        let missions: object[] = Object.values(data.result)
        for (let index = 0; index < missions.length; index++) {
          const element = missions[index];
          console.log('mission_id:' + element['mission_id'])
          console.log('mission_name:' + element['name'])
          this.missionList.push(new Mission(element['mission_id'], element['name']))
        }
        console.info('MissionList:' + JSON.stringify(this.missionList));
      } else {
        console.info('error:' + JSON.stringify(err));
        // 取消订阅HTTP响应头事件
        httpRequest.off('headersReceive');
        // 当该请求使用完毕时，调用destroy方法主动销毁
        httpRequest.destroy();
      }
    }
    );
  }

}

export { componentA, componentB, componentC, componentD, Mission, Marker, componentMarker, MarkerDialog }
