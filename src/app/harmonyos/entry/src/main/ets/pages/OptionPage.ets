import { router, window } from '@kit.ArkUI'
import { common } from '@kit.AbilityKit'
import { mapCommon ,map, MapComponent} from '@kit.MapKit';
import { BusinessError } from '@kit.BasicServicesKit';
import { media } from '@kit.MediaKit';
import { Tasks } from '../entity/Tasks';
import { ArrayList,JSON } from '@kit.ArkTS';
import { rcp } from '@kit.RemoteCommunicationKit';
import { url } from '@kit.ArkTS';
import { interfaceUser, Json_msg } from '../interfaces/InterfaceUser';
import { InterfaceMission } from '../interfaces/InterfaceMission';
import { Mission, Point, TABLE_, TAdd, TEdit, TGet } from '../utils/MysqlUtil';
import { webview } from '@kit.ArkWeb';
import systemDateTime from '@ohos.systemDateTime';
@Entry
@Component
struct OptionPage {
  @State items: string[] = [];
  @State taskFlag:boolean=false;//是否弹出任务框
  @State taskPointFlag:boolean=false;//标点页面弹出
  @State videoFlag:boolean=false;
  private mapController:map.MapComponentController=new map.MapComponentController()//地图控制器
  private controller: webview.WebviewController = new webview.WebviewController();//视频控制器

  //private longitude:number= 118.08683647036881
  //private latitude:number= 24.579691167512674
  //标点数组
  @State pointArr:map.Marker[]=[];
  @State pointArr1:Point[]=[];
  private polyLine:map.MapPolyline | null=null;
  @State tasks:Mission[]=[]
  @State pointArr2:mapCommon.LatLng[]=[]
  @State polyLineArr:map.MapPolyline[] | null=null;
  //下标
  @State markIndex:number=0
  private tasksIndex:number=0

  @State user2:interfaceUser= {
    userId: 0,
    username: '',
    password: '',
    phoneNumber:0,
    devUuidList: '',
    missionIdList: ''
  };



  mapOptions:mapCommon.MapOptions={
    scaleControlsEnabled:true,
    position:{
      target:{
        longitude: 118.08683647036881,
        latitude: 24.579691167512674
      },
      zoom:15
    }
  }
  mapLoad(err:BusinessError,mapController:map.MapComponentController){
    if(err){
      console.log('渲染地图出错'+JSON.stringify(err))
      return;
    }
    this.mapController=mapController;
    this.mapController.setZoomGesturesEnabled(true)//动态设置手势缩放

    this.mapController.on("mapClick",(position)=>this.addMarker(position))
    //this.mapController.on("markerDrag",()=>this.markerDragHandler())
    //this.mapController.on("markerDragStart",()=>this.markerDragHandler())
    //this.mapController.on("mapLoad",()=>this.showPointList())
  }

  aboutToAppear(): void {
    try {
      this.user2=router.getParams() as interfaceUser
    }catch (e){
      console.log("some err exist at aboutToAppear-MainPage")
    }
    let context = getContext(this) as common.UIAbilityContext
    window.getLastWindow(context).then((lastWindow)=> {
      lastWindow.setPreferredOrientation(window.Orientation.LANDSCAPE)
    })
  }

  //添加标记
  addMarker(position:mapCommon.LatLng){
    console.log('添加标记')
    /*let x=Math.random()/10;
    let y=Math.random()/10;
    let lng=this.longitude+x;
    let lat=this.latitude+y;*/
    //构造标记点对象
    let markerOption:mapCommon.MarkerOptions={
      position:position,
      clickable:true,
      title:'随机标记',
      zIndex:2,
    }
    console.log('添加的标记点是：'+JSON.stringify(markerOption))
    this.mapController.addMarker(markerOption).then(result=>{
      console.log('新加入的点'+JSON.stringify(result))
      this.pointArr.push(result)
      this.pointArr2.push(result.getPosition())
      this.addLine()
    }).catch((err:BusinessError)=>{
      console.log('添加标记点失败：'+JSON.stringify(err))
    })
  }

  //添加折线
  addLine(){
    let tem:mapCommon.LatLng[]=[]
    //console.log('1tem'+JSON.stringify(tem))
    this.pointArr.forEach(value=>{
      //console.log('2tem'+JSON.stringify(tem))
      console.log('pointArrPosition'+JSON.stringify(value.getPosition()))
      tem.push(value.getPosition())
      //console.log('3tem'+JSON.stringify(tem))
    })
    //let tem=this.pointArr2
    if(tem.length>=3){
      tem.push(tem[0])
    }
    //构造折线对象
    console.log('4tem:'+JSON.stringify(tem))
    let line:mapCommon.MapPolylineOptions={
      points:tem,
      startCap:1,
      endCap:1,
      width:100,
      color:0xff00ffff,
      jointType:2
    }
    if(!this.polyLine){
      this.mapController.addPolyline(line).then(result=>{
        console.log('添加线段成功：'+JSON.stringify(result))
        this.polyLine=result
      }).catch((err:BusinessError)=>{
        console.log('添加线段失败：'+JSON.stringify(err))
      })
    }else{
      this.polyLine.setPoints(tem)
    }
    //this.polyLine=null
  }

  //线段跟随更新
  markerDragHandler(){
    //console.log('点数组:'+this.pointArr)
    this.addLine()
  }

  //创建任务
  createTask(){
    let index=this.tasks==null?0:this.tasks.length
    let res=TAdd(TABLE_.mission_data,`${index}`,`${this.user2.userId}`,"2018-10-1,13:14:00")
    try {
      systemDateTime.getCurrentTime(true, (error: BusinessError, time: number) => {
        if (error) {
          console.info(`Failed to get currentTime. message: ${error.message}, code: ${error.code}`);
          return;
        }
        console.info(`Succeeded in getting currentTime : ${time}`);
      });
    } catch(e) {
      let error = e as BusinessError;
      console.info(`Failed to get currentTime. message: ${error.message}, code: ${error.code}`);
    }
    res.then((result:boolean)=>{
      console.log(result?'新建成功':"新建失败")
    })
  }

  //获取任务列表
  getTaskList(){
    console.log('getTaskList()')
    let res=TGet(TABLE_.mission_data,"user_id",`${this.user2.userId}`)
    res.then((result:string)=>{
      let tasks1=JSON.parse(result) as Mission[]
      this.tasks=tasks1
      tasks1.forEach((value:Mission,index:number)=>{
        console.log(`任务${index+1},${value.missionId}`)
      })
    })
  }

  //获取任务点列表
  getPointList(){
    this.taskPointFlag=! this.taskPointFlag
    this.pointArr2=[]
    let session = rcp.createSession();
    let IPAddress:string="47.96.237.24";
    let Port:number=8080;
    let _url = url.URL.parseURL
    (`http://${IPAddress}:${Port}/poi/senior_get?tableindex=1&column=mission_id&value=${this.tasks[this.tasksIndex-1].missionId}`);
    let obj:Json_msg= {
      code: 0,
      msg: '',
      Data: ''
    }
    let mission:Mission= {
      missionId: 0,
      userId: 0,
      createTime: '',
      finishTime: '',
      positionList: '',
      status: 0,
      priority: 0,
      waterDataIdList: '',
      navigationIdList: '',
      description: '',
      videoId: 0
    }
    session.get(_url).then((response) => {
      obj = response.toJSON() as Json_msg; //将其解析为Json_msg
      console.log(JSON.stringify(obj.Data));

      let ms = JSON.parse(JSON.stringify(obj.Data)) as Mission[];

      let ListString: string = '';
      ms.forEach((value: Mission) => {
        console.log(value.missionId.toString())
        ListString = value.positionList
      })
      ListString = "[{" + ListString + "}]"
      while (ListString.search("_") != -1) {
        ListString = ListString.replace("_", "},{");
      }
      console.log("ListString:" + (ListString))
      let pl = JSON.parse(ListString) as Point[];
      let pl2 = JSON.parse(ListString) as mapCommon.LatLng[]
      this.pointArr1=pl
      this.pointArr2=pl2
      this.showPointList()
      pl.forEach((value: Point) => {
        console.log(value.latitude + "   " + value.longitude)
      })
    })
  }

  //删除点
  removeMarker(){
    console.log('removeMarker()')
    let temp=0
    let pl=this.pointArr1
    for(let i=0;i<pl.length;i++){
      if(i==this.markIndex){
        temp=i
        break;
      }
    }
    for(let j=temp;j<pl.length;j++){
      pl[j]=pl[j+1]
    }
    pl.length=pl.length-1
    this.pointArr1=pl
    pl.forEach((value:Point)=>{
      console.log(value.latitude+"   "+value.longitude)
    })
    let listString=JSON.stringify(pl)
    while (listString.search("},{") != -1) {
      listString = listString.replace("},{", "_");
    }
    let result:string=""
    for(let i=2;i<listString.length-2;i++){
      result=result+listString[i]
    }
    let id=this.tasks[this.tasksIndex-1].missionId
    console.log(`${id}`)
    console.log('ListString:'+listString)
    console.log('result:'+result)
    let res=TEdit(TABLE_.mission_data,id,"position_list",result)
    res.then((result)=>{
      console.log(result?"操作成功":"操作失败")
    })

  }

  //点击任务后在地图上显示点
  showPointList(){
    console.log('showPointList()')
    if(this.taskFlag&&this.taskPointFlag){
      this.pointArr2.forEach((value)=>{
        this.showMarker(value)
      })
    }else{
      //let temps=this.pointArr
      //console.log('1'+JSON.stringify(this.pointArr.length))
      this.mapController.clear()
      this.polyLine=null
      console.log('数量'+this.pointArr.length)
      for(let j=0;this.pointArr.length%2==0?j<=this.pointArr.length:j<=this.pointArr.length+1;j++){
        for(let i=0;i<this.pointArr.length-1;i++){
          this.pointArr[i]=this.pointArr[i+1]
        }
        this.pointArr.length-=1
      }

      this.pointArr.forEach(value=>{
        console.log(JSON.stringify(value))
      })
    }
  }

  showMarker(position:mapCommon.LatLng){
    console.log('添加标记')
    /*let x=Math.random()/10;
    let y=Math.random()/10;
    let lng=this.longitude+x;
    let lat=this.latitude+y;*/
    //构造标记点对象
    let markerOption:mapCommon.MarkerOptions={
      position:position,
      draggable:true,
      title:'标记',
      zIndex:2,
    }
    console.log('已有的标记点:'+JSON.stringify(markerOption))
    this.mapController.addMarker(markerOption).then(result=>{
      this.pointArr.push(result)
      this.addLine()
    }).catch((err:BusinessError)=>{
      console.log('添加标记点失败：'+JSON.stringify(err))
    })
  }


  build() {
    Stack({ alignContent: Alignment.TopStart }) {
      Row(){
        MapComponent({
          mapOptions: this.mapOptions,
          mapCallback:(err,controller)=>this.mapLoad(err,controller)
        })
      }
      Row(){
        //各种功能弹窗的按钮
        Column(){
          Image($r('app.media.back'))
            .margin({bottom:50,top:20})
            .width(24)
            .height(24)
            .onClick(()=>{
              router.pushUrl({
                url:'pages/Index',
                params:this.user2
              })
            })
          //摄像头
          Image($r('app.media.video'))
            .margin({bottom:10})
            .width(24)
            .height(24)
            .onClick(()=>{
              if(!this.videoFlag){
                this.videoFlag=true
              }else{
                this.videoFlag=false
              }
            })
          //任务
          Image($r('app.media.task'))
            .margin({bottom:10})
            .width(24)
            .height(24)
            .onClick(()=>{
              this.taskFlag=!this.taskFlag
              this.getTaskList()
            })
          Button('手动')
            .margin({ left:50 ,bottom:20})
            .type(ButtonType.Normal)
            .backgroundColor('rgb(225,255,255)')
            .fontColor(Color.Black)
            .onClick(()=>{

            })
          Button('悬停')
            .margin({ left:50 ,bottom:20})
            .type(ButtonType.Normal)
            .backgroundColor('rgb(225,255,255)')
            .fontColor(Color.Black)
            .onClick(()=>{

            })
        }

        //无人艇运行状态
        Row(){
          Column(){
            Text('0.00')
            Text('时速(km/h)')
            //XComponent({ id: 'xcomponentId1', type: 'surface', libraryname: 'nativerender' })

          }
          Column(){
            Text('电量')
          }
        }
        .backgroundColor(Color.White)
        .padding(10)
        .opacity(0.8)
        .position({x:350,y:330})

        //任务列表窗口
        Column(){
          Row(){
            List(){
              ForEach(this.tasks,(val:Mission,index:number)=>{
                ListItem(){
                  Text(`任务${index+1},${val.missionId}`)
                    .margin({top:5,left:5})
                    .onClick(()=>{
                      this.tasksIndex=index+1;
                      this.getPointList()
                    })
                }
              })
            }
            .width(150)
            .height(150)
          }
          Row(){
            Button('+新建任务')
              .onClick(()=>this.createTask())
              .type(ButtonType.Normal)
              .backgroundColor('rgb(220,220,220)')

          }.align(Alignment.Bottom)
        }
        .backgroundColor(Color.White)
        .width(150)
        .height(200)
        .position({x:120,y:100})
        .visibility(this.taskFlag?Visibility.Visible:Visibility.None)

        //任务标点列表窗口
        Column(){
          List(){
            ForEach(this.pointArr2,(val:mapCommon.LatLng,index:number)=>{
              ListItem(){
                Row(){
                  Text(`longitude:${val.longitude},latitude:${val.latitude}`)
                  Image($r('app.media.delete'))
                    .width(24)
                    .height(24)
                    .onClick(()=>{
                      this.markIndex=index
                      this.removeMarker()
                    })
                }
              }
            })
          }
          .height(100)
          Row(){
            Button('完成')
              .onClick(()=>{this.taskPointFlag=! this.taskPointFlag})
              .type(ButtonType.Normal)
              .backgroundColor('rgb(220,220,220)')

          }.align(Alignment.Bottom)
        }
        .width(230)
        .height(150)
        .position({x:580,y:220})
        .visibility(this.taskFlag&&this.taskPointFlag?Visibility.Visible:Visibility.None)
        .backgroundColor(Color.White)
        Column(){
          Web({ src: 'http://47.96.237.24:5000/', controller: this.controller, incognitoMode: true })
          //let video=media.createAVPlayer()
        }
        .width(230)
        .height(150)
        .position({x:580,y:70})
        .visibility(this.videoFlag?Visibility.Visible:Visibility.None)
      }

    }
    .width('100%').height('100%')
    .onClick(()=>this.aboutToAppear())
  }
}


