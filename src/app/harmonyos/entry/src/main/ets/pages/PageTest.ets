import { MapComponent, mapCommon, map } from '@kit.MapKit';
import { AsyncCallback } from '@kit.BasicServicesKit';

@Entry
@Component
struct HuaweiMapDemo {
  private TAG = "HuaweiMapDemo";
  private mapOption?: mapCommon.MapOptions;
  private callback?: AsyncCallback<map.MapComponentController>;
  private mapController?: map.MapComponentController;

  aboutToAppear(): void {
    // 地图初始化参数，设置地图中心点坐标及层级
    this.mapOption = {
      position: {
        target: {
          latitude: 39.9,
          longitude: 116.4
        },
        zoom: 10
      }
    };

    // 地图初始化的回调
    this.callback = async (err, mapController) => {
      if (!err) {
        // 获取地图的控制器类，用来操作地图
        this.mapController = mapController;
        this.mapController.on("mapLoad", () => {
          console.info(this.TAG, `on-mapLoad`);
        });
      }
    };
  }

  // 页面每次显示时触发一次，包括路由过程、应用进入前台等场景，仅@Entry装饰的自定义组件生效
  // onPageShow(): void {
  //   // 绘制地图页面的生命周期onPageShow，将地图切换到前台
  //   if (this.mapController !== undefined) {
  //     this.mapController.show();
  //   }
  // }

  // 页面每次隐藏时触发一次，包括路由过程、应用进入后台等场景，仅@Entry装饰的自定义组件生效。
  // onPageHide(): void {
  //   // 绘制地图页面的生命周期onPageHide，将地图切换到后台
  //   if (this.mapController !== undefined) {
  //     this.mapController.
  //   }}

  build() {
    Stack() {
      // 调用MapComponent组件初始化地图
      MapComponent({ mapOptions: this.mapOption, mapCallback: this.callback }).width('100%').height('100%');
    }.height('100%')
  }
}