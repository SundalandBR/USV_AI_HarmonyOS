export interface interfaceUser{
"userId":number,
"username":string,
"password":string,
"phoneNumber":number,
"devUuidList":string,
"missionIdList":string
}

interface Json_msg {
  "code": number;
  "msg": string;
  "Data": string;
}

export {Json_msg}