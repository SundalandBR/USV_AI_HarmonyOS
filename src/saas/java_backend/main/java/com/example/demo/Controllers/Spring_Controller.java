
package com.example.demo.Controllers;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.example.demo.pojo.*;
import com.example.demo.service.*;
import com.example.demo.service.Impl.TokenServerImpl;
import com.example.demo.vo.Result;
import com.sun.net.httpserver.Request;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.cassandra.CassandraProperties;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.List;



@RestController
@Slf4j
@RequestMapping("/poi")
public class Spring_Controller {





    @Autowired
    private TokenServerImpl tokenServerImpl;
    @Autowired
    private IMissionService MissionService;
    @Autowired
    private IUserService UserService;
    @Autowired
    private INavigationService NavigationService;
    @Autowired
    private IWaterDataService WaterDataService;
    @Autowired
    private IVideoService VideoService;















    @PostMapping("login")
    public Result login(@RequestParam String username,@RequestParam String password, HttpServletRequest request){
        User user=UserService.getOne(new QueryWrapper<User>().eq("user_id", Integer.valueOf(username)));
        log.info("登录验证");
        if(user==null){
            return Result.fail("账号不存在");
        }else{
           if(password.equals(user.password)){
               String ip=request.getRemoteAddr();
               log.info("ip:{}开始添加token<--reids",ip);
               String token=tokenServerImpl.generateToken(ip);
               log.info("添加完毕");
               user.password="***";
               Result<User> t= new Result<>();
               t.code=1;
               t.msg=token;
               t.Data=user;
               return t;
           }else{
               return Result.fail("密码错误");
            }
        }


    }

    @PostMapping("sign")//注册
    public Result sign(@RequestParam String Acc,
                       @RequestParam String psw,
                       @RequestParam String username,
                       @RequestParam String phone){
        User user=UserService.getOne(new QueryWrapper<User>().eq( "user_id",Integer.valueOf(Acc)));
        if(user==null){
            user=new User();
            user.username=username;
            user.userId=Integer.parseInt(Acc);
            user.password=psw;
            user.phoneNumber=phone;
            UserService.save(user);
            user.password="cant be seen";
            return Result.Success(user);
        }else{
            return Result.fail("用户名已经存在");
        }

    }




    @PostMapping("/edit")
    public Result edit(){
        log.info("this is edit");
        return Result.Success();
    }






    @GetMapping("senior_get")//
    public Result senior_get(@RequestParam String tableindex,
                         @RequestParam String column,
                         @RequestParam String value
    ){
        switch (tableindex){
            case "1":{//
                List<Mission> ms=MissionService.list(new QueryWrapper<Mission>().eq(column,value));
                return ms.isEmpty()?Result.fail("未找到"):Result.Success(ms);
            }case "2":{
                List<Navigation> ms=NavigationService.list(new QueryWrapper<Navigation>().eq(column,value));
                return ms.isEmpty()?Result.fail("未找到"):Result.Success(ms);
            }case "3": {
                List<User> ms = UserService.list(new QueryWrapper<User>().eq(column, value));
                return ms.isEmpty() ? Result.fail("未找到") : Result.Success(ms);
            }case "4": {
                List<Video> ms = VideoService.list(new QueryWrapper<Video>().eq(column, value));
                return ms.isEmpty()? Result.fail("未找到") : Result.Success(ms);
            }case "5": {
                List<WaterData> ms =WaterDataService.list(new QueryWrapper<WaterData>().eq(column, value));
                return ms.isEmpty() ? Result.fail("未找到") : Result.Success(ms);
            }
        }
        return Result.Success();
    }


    @PostMapping("senior_editForNavigation")
    public Result senior_editForNavigation(@RequestParam String param1,
                              @RequestParam String param2,
                              @RequestParam String param3,
                              @RequestParam String param4,
                                           @RequestParam String param5,
                                            @RequestParam String param6
    ){

        UpdateWrapper<Navigation> updateWrapper=new UpdateWrapper<>();
        Navigation t=NavigationService.getById(1);
        t.latitude= Double.parseDouble(param1);
        t.longitude= Double.parseDouble(param2);
        t.speed=Float.parseFloat(param3);
        t.course=Float.parseFloat(param4);
        t.status=Integer.valueOf(param5);
        t.batteryLevel=Float.parseFloat(param6);
        updateWrapper.setEntity(t);
        boolean r=NavigationService.update(updateWrapper);
        return r?Result.Success():Result.fail("是");
    };

    @PostMapping("senior_edit")//按Id修改单条数据
    public Result senior_edit(@RequestParam String tableindex,
                              @RequestParam String id,
                             @RequestParam String column,
                             @RequestParam String value
    ){
        switch (tableindex){
            case "1":{
                UpdateWrapper<Mission> updateWrapper=new UpdateWrapper<>();
                updateWrapper.eq("mission_id",id);
                updateWrapper.set(column,value);
                boolean r= MissionService.update(updateWrapper);
                return r?Result.Success():Result.fail("操作失败");
            }case "2":{
                UpdateWrapper<Navigation> updateWrapper=new UpdateWrapper<>();
                updateWrapper.eq("navigation_id",id);
                updateWrapper.set(column,value);
                boolean r= NavigationService.update(updateWrapper);
                return r?Result.Success():Result.fail("操作失败");
            }case "3":{
                UpdateWrapper<User> updateWrapper=new UpdateWrapper<>();
                updateWrapper.eq("user_id",id);
                updateWrapper.set(column,value);
                boolean r= UserService.update(updateWrapper);
                return r?Result.Success():Result.fail("操作失败");
            }case "4":{
                UpdateWrapper<Video> updateWrapper=new UpdateWrapper<>();
                updateWrapper.eq("video_id",id);
                updateWrapper.set(column,value);
                boolean r= VideoService.update(updateWrapper);
                return r?Result.Success():Result.fail("操作失败");
            }case "5":{
                UpdateWrapper<WaterData> updateWrapper=new UpdateWrapper<>();
                updateWrapper.eq("water_data_id",id);
                updateWrapper.set(column,value);
                boolean r= WaterDataService.update(updateWrapper);
                return r?Result.Success():Result.fail("操作失败");
            }
        }
        return Result.Success();
    }



    @DeleteMapping("senior_delete")//
    public Result senior_delete(@RequestParam String tableindex,
                              @RequestParam String id

    ){
        return switch (tableindex) {
            case "1" -> MissionService.removeById(id) ? Result.Success() : Result.fail("操作失败");
            case "2" -> NavigationService.removeById(id) ? Result.Success() : Result.fail("操作失败");
            case "3" -> UserService.removeById(id) ? Result.Success() : Result.fail("操作失败");
            case "4" -> VideoService.removeById(id) ? Result.Success() : Result.fail("操作失败");
            case "5" -> WaterDataService.removeById(id) ? Result.Success() : Result.fail("操作失败");
            default -> Result.Success();
        };
    }

    @PostMapping("senior_add")//插入一条数据
    public  Result senior_add(@RequestParam String tableindex,
                              @RequestParam    String param1,
                              @RequestParam(defaultValue = "") String param2,
                              @RequestParam(defaultValue = "") String param3,
                              @RequestParam(defaultValue = "") String param4,
                              @RequestParam(defaultValue = "") String param5,
                              @RequestParam(defaultValue = "6") String param6,
                              @RequestParam(defaultValue = "7") String param7,
                              @RequestParam(defaultValue = "") String param8,
                              @RequestParam(defaultValue = "") String param9,
                              @RequestParam(defaultValue = "") String param10,
                              @RequestParam(defaultValue = "11") String param11,
                              @RequestParam(defaultValue = "") String param12

    ){
        switch (tableindex){
            case "1":{
                Mission t=new Mission();
                t.missionId=Integer.valueOf(param1);
                t.userId=Integer.valueOf(param2);
                t.createTime=param3;
                t.finishTime=param4;
                t.positionList=param5;
                t.status=Integer.valueOf(param6);
                t.priority=Integer.valueOf(param7);
                t.waterDataIdList=param8;
                t.navigationIdList=param9;
                t.description=param10;
                t.videoId=Integer.parseInt(param11);
                return  MissionService.save(t)?Result.Success():Result.fail("插入失败");
            }
            case "2":{
                Navigation t=new Navigation();
                t.navigationId=Integer.parseInt(param1);
                t.missionId=Integer.valueOf(param2);
                t.timestamp=param3;
                t.latitude= Double.parseDouble(param4);
                t.longitude= Double.parseDouble(param5);
                t.speed=Float.parseFloat(param6);
                t.course=Float.parseFloat(param7);
                t.status=Integer.valueOf(param8);
                t.batteryLevel=Float.parseFloat(param9);
                return  NavigationService.save(t)?Result.Success():Result.fail("插入失败");


            }
            case "3":{
                User t=new User();
                t.userId=Integer.valueOf(param1);
                t.username=param2;
                t.password=param3;
                t.phoneNumber=param4;
                t.devUuidList=param5;
                t.missionIdList=param6;
                return  UserService.save(t)?Result.Success():Result.fail("插入失败");
            }case "4":{
                Video t=new Video();
                t.videoId=Integer.valueOf(param1);
                t.filePath=param2;
                t.fileSize=Integer.parseInt(param3);
                t.duration=Float.parseFloat(param4);
                t.resolution=Float.parseFloat(param5);
                return  VideoService.save(t)?Result.Success():Result.fail("插入失败");
            } case "5":{
                WaterData t=new WaterData();
                t.waterDataId=Integer.valueOf(param1);
                t.missionId=Integer.valueOf(param2);
                t.timestamp=param3;
                t.latitude=Double.parseDouble(param4);
                t.longitude=Double.parseDouble(param5);
                t.ph=Float.parseFloat(param6);
                t.dissolvedOxygen=Float.parseFloat(param7);
                t.conductivity=Float.parseFloat(param8);
                t.temperature=Float.parseFloat(param9);
                t.turbidity=Float.parseFloat(param10);
                t.ammoniaNitrogen=Float.parseFloat(param11);
                t.organicMatter=Float.parseFloat(param12);
                return  WaterDataService.save(t)?Result.Success():Result.fail("插入失败");
            }
        }
        return Result.Success();
    }


    @PostMapping("login_out")
    public Result login_out(HttpServletRequest request){
        log.info("登出验证");
        String token = request.getHeader("Authorization");
        String ip = request.getRemoteAddr();
        boolean r= tokenServerImpl.verifyToken(token,ip) ;
        if(r){
            tokenServerImpl.deleteToken(token);
            boolean r1=tokenServerImpl.verifyToken(token,ip);
            if(r1){
                log.info("还查到了token");
                return Result.fail("失败");
            }else{
                log.info("登出成功");
                return Result.Success();
            }
        }else{
            log.info("这个token和ip不在redis中");
            return Result.fail("操作失败");
        }

    }




}
