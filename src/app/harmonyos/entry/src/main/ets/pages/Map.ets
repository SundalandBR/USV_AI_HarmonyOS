import { MapComponent, mapCommon, map } from '@kit.MapKit';
import { BusinessError } from '@kit.BasicServicesKit';
import { router, window } from '@kit.ArkUI';
import {
  componentA,
  componentB,
  componentC,
  componentD,
  Mission,
  Marker,
  componentMarker,
  MarkerDialog
} from '../utils/Component';
import http from '@ohos.net.http';
import { List } from '@kit.ArkTS';

@Entry
@Component
export struct Map {
  @State @Watch('onCompAShowStatusChange') isShowA: boolean = false;

  onCompAShowStatusChange() {
    // 感知组件显隐
    console.log('监听A组件：' + `${this.isShowA ? '显示' : '隐藏'}`);
  }

  @State isShowB: boolean = false;
  @State isShowD: boolean = false;
  @State list_id: number = 1
  @State private markerArr: map.Marker[] = []
  @State private severIP: string = '172.19.76.146:8087'
  @State private missionList: Mission[] = []
  @State private markerList: Marker[] = []
  private mapController: map.MapComponentController = new map.MapComponentController();
  private mapOptions: mapCommon.MapOptions = {
    scaleControlsEnabled: true, //显示比例尺
    position: {
      target: {
        longitude: 118.08683647036881,
        latitude: 24.579691167512674
      },
      zoom: 15//[2,20] 地图缩放级别
    }
  }

  aboutToAppear() {
    // 调用时临时旋转到横屏，之后跟随传感器自动旋转
    // 受控制中心的旋转开关控制，且可旋转方向受系统判定
    this.setOrientation(14);
  }

  /**
   * 设置旋转策略
   */
  setOrientation(orientation: number) {
    window.getLastWindow(getContext(this)).then((win) => {
      win.setPreferredOrientation(orientation).then((data) => {
        console.log('setWindowOrientation: ' + orientation + ' Succeeded. Data: ' + JSON.stringify(data));
      }).catch((err: string) => {
        console.log('setWindowOrientation: Failed. Cause: ' + JSON.stringify(err));
      });
    }).catch((err: string) => {
      console.log('setWindowOrientation： Failed to obtain the top window. Cause: ' + JSON.stringify(err));
    });
  }

  mapLoad(err: BusinessError, mapController: map.MapComponentController) {
    //console.log('地图创建')
    if (err) {
      console.error('地图渲染出错：' + JSON.stringify(err))
    }
    this.mapController = mapController
  }

  mapClickHandler(position: mapCommon.LatLng) {
    this.newMarker(position)
  }

  newMarker(position: mapCommon.LatLng) {
    //在点击位置创建一个点 标记图片显示不全是模拟器的问题
    let markerOption: mapCommon.MarkerOptions = {
      position: position,
      draggable: true,
      clickable: true
    }
    this.mapController.addMarker(markerOption).then(res => {
      console.log('标记点位：' + JSON.stringify(res.getPosition()))
      this.markerArr.push(res)
    }).catch((err: BusinessError) => {
      console.error('标记失败' + JSON.stringify(err))
    })
  }

  build() {
    Stack({ alignContent: Alignment.TopStart }) {
      //创建地图
      MapComponent({
        mapOptions: this.mapOptions,
        //调用函数的格式不能写为this.mapLoad，要写为()=>{}格式，否则在变量作用域方面会出错
        mapCallback: (err, mapController) => this.mapLoad(err, mapController)
      })
      Column({ space: 5 }) {
        Image($r('app.media.back')).width(30).height(30).onClick(() => {
          router.back()
        })
        Image($r('app.media.video')).width(45).height(45).onClick(() => {
          this.isShowB = !this.isShowB;
        })
        Image($r('app.media.task')).width(45).height(45).onClick(() => {
          //先加载再显示
          if (!this.isShowD) {
            this.loadMissionList()
          } else {
            //每次关闭窗口清空数据
            this.missionList = []
          }
          this.isShowD = !this.isShowD;
        })
        Button("手动").width('100%').onClick(() => {

        })
        Button("悬停").width('100%').onClick(() => {

        })
        Button("传感器").width('100%').onClick(() => {
          this.isShowA = !this.isShowA;
        })
      }.width('10%').margin({ top: 10, left: 10 })

      if (this.isShowA) {
        componentA();
      }
      if (this.isShowB) {
        componentB();
      }
      if (this.isShowD) {
        componentD({
          missionList: this.missionList,
          markerList: this.markerList,
          severIP: this.severIP,
          mapController: this.mapController,
          markerArr: this.markerArr,
          list_id: this.list_id
        });
      }
      componentC();
    }
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
        //data为JSON类型，属性可以直接取，打印不用先转换为字符串
        // console.info('data:' + JSON.stringify(data));
        //let list = data.result
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
        /*this.missions = data.result
        this.missions.forEach*/
        /*this.missionList.add(data.result[1])
        this.missionList.forEach((value: Object, index?: number) => {
          console.log("value:" + JSON.stringify(value), "index:" + index);
        });*/
        // console.info('code:' + data.responseCode);
        // console.info('header:' + data.header);
        // console.info('cookies:' + data.cookies); // 8+
        // let result = data.result

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

