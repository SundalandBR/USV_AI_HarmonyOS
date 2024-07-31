export class WaterData{
  waterDataId:number;
  missionId:number;
  time:string;
  latitude:number;
  longitude:number;
  pH:number
  dissolvedOxygen:number
  conductivity:number
  temperature:number
  turbidity:number
  ammoniaNitrogen:number
  organicMatter:number

  constructor(waterDataId: number, missionId: number, time: string, latitude: number, longitude: number, pH: number,
    dissolvedOxygen: number, conductivity: number, temperature: number, turbidity: number, ammoniaNitrogen: number,
    organicMatter: number) {
    this.waterDataId = waterDataId;
    this.missionId = missionId;
    this.time = time;
    this.latitude = latitude;
    this.longitude = longitude;
    this.pH = pH;
    this.dissolvedOxygen = dissolvedOxygen;
    this.conductivity = conductivity;
    this.temperature = temperature;
    this.turbidity = turbidity;
    this.ammoniaNitrogen = ammoniaNitrogen;
    this.organicMatter = organicMatter;
  }

}
