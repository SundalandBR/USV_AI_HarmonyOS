import { JSON } from '@kit.ArkTS';
import { JsonTo32Hex,_8HexToJson} from 'libentry.so';

//mav_cmd=0
export interface HeartbeatT{
  mav_cmd: number,
  type: number,
  autopilot: number,
  base_mode: number,
  custom_mode: number,
  system_status: number,
  mavlink_version: number
}

export function CreateHeartbeatT(type: number,autopilot: number,base_mode: number,custom_mode: number,system_status: number,mavlink_version: number):HeartbeatT{
  return {
    mav_cmd: 0,
    type: type,
    autopilot: autopilot,
    base_mode: base_mode,
    custom_mode: custom_mode,
    system_status: system_status,
    mavlink_version: mavlink_version
  }
}

//mav_cmd=11
export interface SetModeT{
  mav_cmd: number,
  target_system: number,
  base_mode: number,
  custom_mode: number
}

export function CreateSetModeT(base_mode: number,custom_mode: number):SetModeT{
  return {
    mav_cmd: 11,
    target_system: 1,
    base_mode: base_mode,
    custom_mode: custom_mode
  }
}

//mav_cmd=21
export interface ParamRequestListT{
  mav_cmd: number,
  target_system: number,
  target_component: number
}

export function CreateParamRequestListT():ParamRequestListT{
  return {
    mav_cmd:21,
    target_system:1,
    target_component:1
  }
}

//mav_cmd=22
export  interface ParamValueT{
  mav_cmd: number,
  param_id: string,
  param_value: number,
  param_type: number,
  param_count: number,
  param_index: number
}

export function CreateParamValueT(param_id:string,param_value:number,param_type:number,param_count:number,param_index:number):ParamValueT{
  return {
    mav_cmd: 22,
    param_id:param_id,
    param_value:param_value,
    param_type:param_type,
    param_count:param_count,
    param_index:param_index
  }
}

//mav_cmd=24
export interface GpsRawIntT{
  mav_cmd: number,
  time_usec: number,
  fix_type: number,
  lat: number,
  lon: number,
  alt: number,
  eph: number,
  epv: number,
  vel: number,
  cog: number,
  satellites_visible: number,
  alt_ellipsoid: number,
  h_acc: number,
  v_acc: number,
  vel_acc: number,
  hdg_acc: number,
  yaw: number
}

//mav_cmd=30
export interface AttitudeT{
  time_boot_ms: number,
  roll: number,
  pitch: number,
  yaw: number,
  rollspeed: number,
  pitchspeed: number,
  yawspeed: number
}

//mav_cmd=38
export interface MissionWritePartialListT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  start_index: number,
  end_index: number,
  mission_type: number
}

export function CreateMissionWritePartialListT(start_index: number,end_index: number,mission_type: number):MissionWritePartialListT{
  return {
    mav_cmd: 38,
    target_system: 1,
    target_component: 1,
    start_index: start_index,
    end_index: end_index,
    mission_type: mission_type
  }
}

//mav_cmd=39
export interface MissionItemT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  seq: number,
  frame: number,
  command: number,
  current: number,
  autocontinue: number,
  param1: number,
  param2: number,
  param3: number,
  param4: number,
  x: number,
  y: number,
  z: number,
  mission_type: number
}

export function CreateMissionItemT(seq: number,frame: number,command: number,current: number,autocontinue: number,param1: number,param2: number,param3: number,param4: number,x: number,y: number,z: number,mission_type: number): MissionItemT{
  return {
    mav_cmd: 39,
    target_system: 1,
    target_component: 1,
    seq: seq,
    frame: frame,
    command: command,
    current: current,
    autocontinue: autocontinue,
    param1: param1,
    param2: param2,
    param3: param3,
    param4: param4,
    x: x,
    y: y,
    z: z,
    mission_type: mission_type
  }
}

//mav_cmd=40
export interface MissionRequestT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  seq: number,
  mission_type: number
}

export function CreateMissionRequestT(seq: number,mission_type: number): MissionRequestT{
  return {
    mav_cmd: 40,
    target_system: 1,
    target_component: 1,
    seq: seq,
    mission_type: mission_type
  }
}

//mav_cmd=41
export interface MissionSetCurrentT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  seq: number
}

export function CreateMissionSetCurrentT(seq: number): MissionSetCurrentT{
  return {
    mav_cmd: 41,
    target_system: 1,
    target_component: 1,
    seq: seq
  }
}

//mav_cmd=43
export interface MissionRequestListT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  mission_type: number
}

export function CreateMissionRequestListT(mission_type: number): MissionRequestListT{
  return {
    mav_cmd: 43,
    target_system: 1,
    target_component: 1,
    mission_type: mission_type
  }
}

//mav_cmd=44
export interface MissionCountT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  count: number,
  mission_type: number
}

export function CreateMissionCountT(count: number,mission_type: number): MissionCountT{
  return {
    mav_cmd: 44,
    target_system: 1,
    target_component: 1,
    count: count,
    mission_type: mission_type
  }
}

//mav_cmd=45
export interface MissionClearAllT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  mission_type: number
}

export function CreateMissionClearAllT(mission_type: number): MissionClearAllT{
  return {
    mav_cmd: 45,
    target_system: 1,
    target_component: 1,
    mission_type: mission_type
  }
}

//mav_cmd=47
export interface MissionAckT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  type: number,
  mission_type: number
}

export function CreateMissionAckT(type: number,mission_type: number): MissionAckT{
  return {
    mav_cmd: 47,
    target_system: 1,
    target_component: 1,
    type: type,
    mission_type: mission_type
  }
}

//mav_cmd=51
export interface MissionRequestIntT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  seq: number,
  mission_type: number
}

export function CreateMissionRequestIntT(seq: number,mission_type: number): MissionRequestIntT{
  return {
    mav_cmd: 51,
    target_system: 1,
    target_component: 1,
    seq: seq,
    mission_type: mission_type
  }
}

//mav_cmd=66
export interface RequestDataStreamT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  req_stream_id: number,
  start_stop: number
}

export function CreateRequestDataStreamT(req_stream_id:number,start_stop:number):RequestDataStreamT{
  return {
    mav_cmd: 66,
    target_system: 1,
    target_component: 1,
    req_stream_id: req_stream_id,
    start_stop: start_stop
  }
}

//mav_cmd=73
export interface MissionItemIntT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  seq: number,
  frame: number,
  command: number,
  current: number,
  autocontinue: number,
  param1: number,
  param2: number,
  param3: number,
  param4: number,
  x: number,
  y: number,
  z: number,
  mission_type: number
}

export function CreateMissionItemIntT(seq: number,frame: number,command: number,current: number,autocontinue: number,param1: number,param2: number,param3: number,param4: number,x: number,y: number,z: number,mission_type: number): MissionItemIntT{
  return {
    mav_cmd: 73,
    target_system: 1,
    target_component: 1,
    seq: seq,
    frame: frame,
    command: command,
    current: current,
    autocontinue: autocontinue,
    param1: param1,
    param2: param2,
    param3: param3,
    param4: param4,
    x: x,
    y: y,
    z: z,
    mission_type: mission_type
  }
}

//mav_cmd=74
export interface VfrHud{
  mav_cmd: number,
  airspeed: number,
  groundspeed: number,
  heading: number,
  throttle: number,
  alt: number,
  climb: number
}

//mav_cmd=76
export interface CommandLongT{
  mav_cmd: number,
  target_system: number,
  target_component: number,
  command: number,
  confirmation: number,
  param1: number,
  param2: number,
  param3: number,
  param4: number,
  param5: number,
  param6: number,
  param7: number
}

export function CreateCommandLongT(command:number,confirmation:number,param1: number,param2: number,param3: number,param4: number,param5: number,param6: number,param7: number):CommandLongT{
  return {
    mav_cmd:76,
    target_system:1,
    target_component:1,
    command,
    confirmation,
    param1,
    param2,
    param3,
    param4,
    param5,
    param6,
    param7
  }
}

//mav_cmd=147
export interface BatteryStatusT{
  mav_cmd: number,
  id: number,
  battery_function: number,
  type: number,
  temperature: number,
  voltages: Uint16Array,
  current_battery: number,
  current_consumed: number,
  energy_consumed: number,
  battery_remaining: number,
  time_remaining: number,
  charge_state: number,
  voltages_ext: Uint16Array,
  mode: number,
  fault_bitmask: number
}


export function JsonToHex(root: string):Uint8Array{
  let obj=JsonTo32Hex(root);
  let ret=new Uint8Array(obj.length);
  for(let i=0;i<obj.length;i++){
    ret[i]=obj[i];
  }
  return ret;
}

export function HexToJson(root:ArrayBuffer):string{
  return _8HexToJson(root);
}