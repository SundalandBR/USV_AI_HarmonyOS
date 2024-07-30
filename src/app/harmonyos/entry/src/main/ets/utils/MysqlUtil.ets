import { rcp } from '@kit.RemoteCommunicationKit';
import { url } from '@kit.ArkTS';
import { BusinessError } from '@kit.BasicServicesKit';

let IPAddress:string="47.96.237.24";
let Port:number=8080;


enum TABLE_ {
  mission_data = 1,
  navigation_data,
  user_accounts,
  video_data,
  water_quality_data
}

interface Json_msg {
  "code": number;
  "msg": string;
  "Data": string;
}
interface Point{
  "latitude": string,
  "longitude": string
}

interface WaterData{
  "waterDataId": number,
  "missionId": number,
  "timestamp": string,
  "latitude": number,
  "longitude": number,
  "ph": number,
  "dissolvedOxygen": number,
  "conductivity": number,
  "turbidity": number,
  "ammoniaNitrogen": number,
  "organicMatter": number
}
interface  Mission{
  "missionId":number;
  "userId":number;
  "createTime":string;
  "finishTime":string;
  "positionList":string;
  "status":number;
  "priority":number;//优先级
  "waterDataIdList":string;
  "navigationIdList":string;
  "description":string;
  "videoId":number;
}








async  function TAdd(tableIndex:TABLE_, param1:string,param2:string,param3:string,
  param4:string="0",param5:string="0",param6:string="0",
  param7:string="0",param8:string="0",param9:string="0",
  param10:string="0",param11:string="0",param12:string="0"
):Promise<boolean>{

  console.log("TAdd has been called")
  let obj:null|Json_msg=null;
  let session = rcp.createSession();
  let _url = url.URL.parseURL(`http://${IPAddress}:${Port}/poi/senior_add?tableindex=${tableIndex}&param1=${param1}&param2=${param2}&param3=${param3}&param4=${param4}&param5=${param5}&param6=${param6}&param7=${param7}&param8=${param8}&param9=${param9}&param10=${param10}&param11=${param11}&param12=${param12}`);
  console.log(_url.toString())
  session.post(_url).then((response) => {
    console.log(JSON.stringify(response));
    obj=response.toJSON() as Json_msg;//将其解析为Json_msg

  }).catch((err: BusinessError) => {
    console.error(`err: err code is ${err.code}, err message is ${JSON.stringify(err)}`);
  });
  const result: boolean = await new Promise((resolve: Function) => {
    setTimeout(() => {
      resolve(obj?.code==1)
    }, 1000);
  });
  return result;

}




async function TDelete(table:TABLE_,id:number):Promise<boolean>{
  let obj:Json_msg= {
    code: 0,
    msg: '',
    Data: ''
  }
  let session = rcp.createSession();
  // delete
  let _url = url.URL.parseURL(`http://${IPAddress}:${Port}/poi/senior_delete?tableindex=${table}&id=${id}`);
  console.log(JSON.stringify(_url))
  session.delete(_url).then((response)=>{
    obj=response.toJSON() as Json_msg;
  }).catch((err: BusinessError) => {
    console.error(`err: err code is ${err.code}, err message is ${JSON.stringify(err)}`);
  });
  const result:boolean=await  new Promise((resolve:Function)=>{
    setTimeout(()=>{
      resolve(obj.code==1)
    },1500)
  });
  return result;
}



async function TGet(TableIndex:TABLE_,column:string,value:string):Promise<string>{
  let session = rcp.createSession();
  let _url = url.URL.parseURL(`http://${IPAddress}:${Port}/poi/senior_get?tableindex=${TableIndex}&column=${column}&value=${value}`);
  let obj:Json_msg= {
    code: 0,
    msg: '',
    Data: ''
  }
  session.get(_url).then((response) => {
    obj=response.toJSON() as Json_msg;//将其解析为Json_msg
  }).catch((err: BusinessError) => {
    console.error(`err: err code is ${err.code}, err message is ${JSON.stringify(err)}`);
  });
  const result: string = await new Promise((resolve: Function) => {
    setTimeout(() => {
      resolve(JSON.stringify(obj.Data)==""?"请求超时":JSON.stringify(obj.Data))
    }, 3000);
  });
  return result;
}

async function TEdit(tableIndex:TABLE_,Id:number,column:string,value:string):Promise<boolean>{
  let session = rcp.createSession();
  let obj:Json_msg= {
    code: 0,
    msg: '',
    Data: ''
  }//senior_edit
  let _url = url.URL.parseURL(`http://${IPAddress}:${Port}/poi/senior_edit?tableindex=${tableIndex}&id=${Id}&column=${column}&value=${value}`);
  session.post(_url).then((response)=>{
    obj=response.toJSON() as Json_msg;
    console.log(JSON.stringify(obj))

  })
  const result:boolean=await new  Promise((resolve:Function)=>{
    setTimeout(()=>{
      resolve(obj.code==1)
    },1500)
  })
  return result ;
}
export{TGet,TAdd,TDelete,TEdit,WaterData,Point,Mission,IPAddress,Port,TABLE_}
