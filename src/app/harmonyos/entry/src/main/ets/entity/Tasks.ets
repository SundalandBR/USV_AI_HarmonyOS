import {map, mapCommon } from '@kit.MapKit'
import { Navigation } from './Navigation';
import { WaterData } from './WaterData';
import { ArrayList } from '@kit.ArkTS';


export class Tasks{
  missionId:number;
  userId:number;
  createTime:string;
  finishTime:string;
  positionList:mapCommon.LatLng[];
  status:string;
  priority:string;
  waterDataList:WaterData[];
  navigationList:Navigation[];
  description:string;

  constructor(missionId: number, userId: number, createTime: string, finishTime: string,
    positionList: mapCommon.LatLng[], status: string, priority: string, waterDataList: WaterData[],
    navigationList: Navigation[], description: string) {
    this.missionId = missionId;
    this.userId = userId;
    this.createTime = createTime;
    this.finishTime = finishTime;
    this.positionList = positionList;
    this.status = status;
    this.priority = priority;
    this.waterDataList = waterDataList;
    this.navigationList = navigationList;
    this.description = description;
  }




}