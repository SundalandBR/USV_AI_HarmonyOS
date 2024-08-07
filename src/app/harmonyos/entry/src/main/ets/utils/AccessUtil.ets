import { abilityAccessCtrl, bundleManager, common, Permissions, Want } from '@kit.AbilityKit'
import { ble } from '@kit.ConnectivityKit';
import { mapCommon ,map, MapComponent} from '@kit.MapKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { CommandLongT, CreateCommandLongT,
  CreateMissionCountT,
  CreateMissionItemIntT,
  HexToJson, JsonToHex,
  MissionAckT,
  MissionCountT,
  MissionItemIntT} from '../interfaces/MavLink_Data';
import { promptAction } from '@kit.ArkUI';
import { buffer } from '@kit.ArkTS';
import { BusinessError,  } from '@kit.BasicServicesKit';

//判断是否有权限
function checkPermissionGrant(permission:Permissions):Boolean{
  let bundleInfo:bundleManager.BundleInfo=bundleManager.getBundleInfoForSelfSync(bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_APPLICATION);
  let appInfo=bundleInfo.appInfo;
  let tokenId=appInfo.accessTokenId;
  let atManager=abilityAccessCtrl.createAtManager();
  let status:abilityAccessCtrl.GrantStatus=atManager.verifyAccessTokenSync(tokenId,permission);
  return status==abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED
}

//向用户申请权限
function requestPermissionsFromUser(context:common.UIAbilityContext,permissions:Permissions[],request:string){
  let atManager=abilityAccessCtrl.createAtManager();
  atManager.requestPermissionsFromUser(context,permissions).then((result)=>{
    let r=result.authResults;
    let arr:number[]=[]
    r.forEach((res:number)=>{
      console.log(permissions[0]+'授权结果:'+res)
      if (res!=abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED) {
        arr.push(res);
      }
    })
    if(arr.length){
      AlertDialog.show({
        message:'此服务需要获取'+request+'信息，请到设置里授予'+request+'权限',
        autoCancel:true,
        alignment:DialogAlignment.Bottom,
        gridCount:4,
        offset:{dx:0,dy:-20},
        primaryButton:{
          value:'返回',
          action:()=>{

          }
        },
        secondaryButton:{
          enabled:true,
          defaultFocus:true,
          style:DialogButtonStyle.HIGHLIGHT,
          value:'同意',
          action:()=>{
            openPermissionInSystemSettings(context);
          }
        },
        cancel: () => {
          console.info('Closed callbacks')
        },
        onWillDismiss:(dismissDialogAction: DismissDialogAction)=> {
          console.info("reason=" + JSON.stringify(dismissDialogAction.reason))
          console.log("dialog onWillDismiss")
          if (dismissDialogAction.reason == DismissReason.PRESS_BACK) {
            dismissDialogAction.dismiss()
          }
          if (dismissDialogAction.reason == DismissReason.TOUCH_OUTSIDE) {
            dismissDialogAction.dismiss()
          }
        }
      })
    }
  })
}

//二次申请拉取其他ability
function openPermissionInSystemSettings(context:common.UIAbilityContext){
  let want:Want={
    bundleName:"com.huawei.hmos.settings",
    abilityName:"com.huawei.hmos.settings.MainAbility",
    uri:"application_info_entry",
    parameters:{
      pushParams:"com.example.wurenting"
    }
  }
  context.startAbility(want)
}


export{checkPermissionGrant,requestPermissionsFromUser,openPermissionInSystemSettings}