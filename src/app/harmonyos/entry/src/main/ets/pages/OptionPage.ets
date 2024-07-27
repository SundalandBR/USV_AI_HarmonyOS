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

@Entry
@Component
struct OptionPage {
  @State items: string[] = [];
  @State taskFlag:boolean=false;//是否弹出任务框
  @State taskPointFlag:boolean=true;//标点页面弹出
  @State videoFlag:boolean=false;
  private mapController:map.MapComponentController=new map.MapComponentController()//地图控制器
  private longitude:number= 118.08683647036881
  private latitude:number= 24.579691167512674
  @State pointArr:map.Marker[]=[];//标点数组
  private arr:ArrayList<map.Marker>|null=null;
  private polyLine:map.MapPolyline | null=null;
  @State tasks:Tasks[]=[]

  private tasksIndex:number=0


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
    this.mapController.on("markerDrag",()=>this.markerDragHandler())
    this.mapController.on("markerDragStart",()=>this.markerDragHandler())

  }

  aboutToAppear(): void {
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
      draggable:true,
      title:'随机标记',
      zIndex:2,
    }
    console.log('添加的标记点是：'+JSON.stringify(markerOption))
    this.mapController.addMarker(markerOption).then(result=>{
      console.log('新加入的点'+JSON.stringify(result))
      this.pointArr.push(result)
      //this.pointArr.push(result)
      this.addLine()
    }).catch((err:BusinessError)=>{
      console.log('添加标记点失败：'+JSON.stringify(err))
    })



  }

  //添加折线
  addLine(){

    /*for(let i=0;i<10;i++){
      let lng=this.longitude+Math.random()/10;
      let lat=this.latitude+Math.random()/10;
      pointArr.push({latitude:lat,longitude:lng})
    }*/
    let tem=this.pointArr.map(v=>v.getPosition())
    if(tem.length>=3){
      tem.push(tem[0])

    }
    //构造折线对象
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

  }

  //线段跟随更新
  markerDragHandler(){
    //console.log('点数组:'+this.pointArr)
    this.addLine()
  }

  //创建任务
  createTask(id:number,name:string,pointArr:map.Marker[]){

  }

  //获取任务列表
  getTaskList(){
    let session=rcp.createSession();
    let _url=url.URL.parseURL(`http://47.96.237.24:8080/poi/getTaskList`)

    session.post(_url).then((response)=>{
      try {
        let obj=response.toJSON() as Json_msg;
        console.log(response.toString());
        console.log("obj.code:"+obj.code)
        console.log("obj.msg:"+obj.msg)
        console.log("obj.Data:"+JSON.stringify(obj.Data))
        let temp=JSON.stringify(obj.Data)
        //let task=JSON.parse(temp) as InterfaceMission
        this.tasks.push(JSON.parse(temp) as Tasks)
        console.log(`${this.tasks}`)
      }catch (err){
        console.log(`json content:${JSON.stringify(err)}}`)
      }
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
                url:'pages/Index'
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
              if(!this.taskFlag){
                this.taskFlag=true
                console.log('taskFlag:'+this.taskFlag)
              }else{
                this.taskFlag=false
                console.log('taskFlag:'+this.taskFlag)
              }
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
          Button('传感器')
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
              ForEach(this.tasks,(val:Tasks)=>{
                ListItem(){
                  Text(`${val.missionId}`)
                    .margin({top:5,left:5})
                    .onClick(()=>{
                      this.tasksIndex=val.missionId
                      if(!this.taskPointFlag){
                        this.taskPointFlag=true
                        console.log('taskPointFlag:'+this.taskPointFlag)
                      }else{
                        this.taskPointFlag=false
                        console.log('taskPointFlag:'+this.taskPointFlag)
                      }
                    })
                }

              })
            }
            .width(150)
            .height(150)
          }
          Row(){
            Button('+新建任务')
              .onClick(()=>this.createTask(1,'任务2',this.pointArr))
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
            ForEach(this.pointArr,(val:map.Marker)=>{
              ListItem(){
                Row(){
                  Text(`longitude:${val.getPosition().longitude},latitude:${val.getPosition().latitude}`)
                    .margin({right:20})
                  Image($r('app.media.delete'))
                    .width(24)
                    .height(24)
                    .onClick(()=>{
                      this.arr?.remove(val)
                    })
                }
              }
            })
          }
          .height(100)
          Row(){
            Button('完成')
              .onClick(()=>{
                if(!this.taskPointFlag){
                  this.taskPointFlag=true
                }else{
                  this.taskPointFlag=false
                }
              })
              .type(ButtonType.Normal)
              .backgroundColor('rgb(220,220,220)')

          }.align(Alignment.Bottom)
        }
        .width(200)
        .height(150)
        .position({x:630,y:220})
        .visibility(this.taskFlag&&this.taskPointFlag?Visibility.Visible:Visibility.None)
        .backgroundColor(Color.White)
        Column(){

          //let video=media.createAVPlayer()
        }
      }

    }
    .width('100%').height('100%')
    .onClick(()=>this.aboutToAppear())
  }
}


