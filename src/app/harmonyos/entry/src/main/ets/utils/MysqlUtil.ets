import { rcp } from '@kit.RemoteCommunicationKit';
import { url } from '@kit.ArkTS';
import { BusinessError } from '@kit.BasicServicesKit';

let IPAddress:string="47.96.237.24";
let Port:number=8080;
export let Token_AAA:string="abc";

export function setToken(Token:string){
  Token_AAA=Token
}


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
  "temperature":number,
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

interface Navigation{
  "navigationId":number
  "missionId":number
  "timestamp":string
  "latitude":number
  "longitude":number
  "speed":number
  "course":number
  "status":number
  "batteryLevel":number
}


async function LoginOut(callback:Callback<boolean>) {
  let session = rcp.createSession({ headers: { "Authorization": Token_AAA } });
  let _url = url.URL.parseURL(`http://${IPAddress}:${Port}/poi/login_out`);
  let obj: Json_msg = {
    code: 0,
    msg: '',
    Data: ''
  }
  await session.post(_url).then((response) => {
    if (response.toString() != null) {
      obj = response.toJSON() as Json_msg;
      callback(obj.code == 1)
    } else {
      callback(false)
    }
  }).catch((err: BusinessError) => {
    console.error(`err: err code is ${err.code}, err message is ${JSON.stringify(err)}`);
  });
}

async  function TAdd(tableIndex:TABLE_, param1:string,param2:string,param3:string,
  param4:string="0",param5:string="0",param6:string="0",
  param7:string="0",param8:string="0",param9:string="0",
  param10:string="0",param11:string="0",param12:string="0"
  ):Promise<boolean>{

  console.log("TAdd has been called")
  let obj:null|Json_msg=null;
  let session = rcp.createSession({headers: {"Authorization": Token_AAA, }});
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
      try {
        //因为返回可能为空,所以此时obj不能引用(这里我是用try-catch)
        resolve(obj?.code==0?"请求超时": JSON.stringify(obj?.Data))
      } catch (e) {
        resolve("操作失败")
      }
    }, 2000);
  });
  return result;

}




async function TDelete(table:TABLE_,id:number):Promise<boolean>{
  let obj:Json_msg= {
    code: 0,
    msg: '',
    Data: ''
  }
  let session = rcp.createSession({headers: {"Authorization": Token_AAA, }});
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
      try {
        //因为返回可能为空,所以此时obj不能引用(这里我是用try-catch)
        resolve(obj?.code==0?"请求超时": JSON.stringify(obj?.Data))
      } catch (e) {
        resolve("操作失败")
      }
    },1500)
  });
  return result;
}



async function TGet(TableIndex:TABLE_,column:string,value:string):Promise<string>{
  let session = rcp.createSession({headers: {"Authorization": Token_AAA, }});
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
      try {
        //因为返回可能为空,所以此时obj不能引用(这里我是用try-catch)
        resolve(obj?.code==0?"请求超时": JSON.stringify(obj?.Data))
      } catch (e) {
        resolve("操作失败")
      }
    }, 3000);
  });
  return result;
}

async function TEdit(tableIndex:TABLE_,Id:number,column:string,value:string):Promise<boolean>{
  let session = rcp.createSession({headers: {"Authorization": Token_AAA, }});
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
      try {
        //因为返回可能为空,所以此时obj不能引用(这里我是用try-catch)
        resolve(obj?.code==0?"请求超时": JSON.stringify(obj?.Data))
      } catch (e) {
        resolve("操作失败")
      }
    },1500)
  })
  return result;
}

async function GetResponseForNavigation(callback:Callback<string>){
  let session = rcp.createSession({headers: {"Authorization": Token_AAA, }});
  let _url = url.URL.parseURL(`http://47.96.237.24:5000/text_feed`);
  await  session.get(_url).then((response) => {
    callback(response.toString())
  }).catch((err: BusinessError) => {
    console.error(`err: err code is ${err.code}, err message is ${JSON.stringify(err)}`);
  });
}

export{LoginOut,TGet,TAdd,TDelete,TEdit,WaterData,Point,Mission,IPAddress,Port,TABLE_,GetResponseForNavigation,Navigation}
