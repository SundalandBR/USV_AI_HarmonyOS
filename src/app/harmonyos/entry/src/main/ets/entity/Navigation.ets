export class Navigation{
  navigationId:number
  missionId:number
  time:string
  latitude:number
  longitude:number
  speed:number
  course:number
  status:number
  batteryLevel:number

  constructor(navigationId: number, missionId: number, time: string, latitude: number, longitude: number, speed: number,
    course: number, status: number, batteryLevel: number) {
    this.navigationId = navigationId
    this.missionId = missionId
    this.time = time
    this.latitude = latitude
    this.longitude = longitude
    this.speed = speed
    this.course = course
    this.status = status
    this.batteryLevel = batteryLevel
  }

}