#include <iostream>

#include "Http/httplib.h"
#include "Data/Data.hpp"
#include "Config.hpp"

using namespace std;
using namespace httplib;
using namespace data;
using namespace config;

//解析get请求后面的参数
json parse_get(const Request& req)
{
    json j;
    for(auto it=req.params.begin();it!=req.params.end();it++){
        j[it->first]=it->second;
    }
    return std::move(j);
}

int main(int argc,char* argv[])
{   
    if(argc!=2){
        fprintf(stderr,"Usage: %s *.conf\n",argv[0]);
        exit(-1);
    }
    Server server;
    Config cfg(argv[1]);
    string url=cfg.get("url");
    string user=cfg.get("user");
    string password=cfg.get("password");
    string databasename=cfg.get("databasename");

    ///登录
    server.Post("/userLogin",[&](const Request& req,Response& res){
        BasicData* data=new Login(url,user,password,databasename);
        json res_j;
        data->Execute(json::parse(req.body.c_str()),res_j);
        res.set_content(res_j.dump(),"text/json");
        //res.set_content("tt","text/plain");
        delete data;
    });

    ///注册
    server.Post("/userSignup",[&](const Request& req,Response& res){
        BasicData* data=new SignUp(url,user,password,databasename);
        json res_j;
        data->Execute(json::parse(req.body.c_str()),res_j);
        res.set_content(res_j.dump(),"text/json");
        //res.set_content("tt","text/plain");
        delete data;
    });

    //获取具体的水质检测数据
    server.Get("/downloadData",[&](const Request& req,Response& res){
        BasicData* data=new DownloadWaterData(url,user,password,databasename);
        json res_j;
        data->Execute(parse_get(req),res_j);
        res.set_content(res_j.dump(),"text/json");
        delete data;
    });

    //获取所有水质检测数据
    server.Get("/showData",[&](const Request& ,Response& res){
        BasicData* data=new ShowWaterData(url,user,password,databasename);
        json res_j;
        data->Execute({},res_j);
        res.set_content(res_j.dump(),"text/json");
        delete data;
    });

    //增加数据库对外接口
    server.Post("/operatorMysql",[&](const Request& req,Response& res){
        BasicData* data=new OperatorMysql(url,user,password,databasename);
        json res_j,req_j=json::parse(req.body.c_str());
        data->Execute(req_j,res_j);
        res.set_content(res_j.dump(),"text/json");
        delete data;
    });

    server.listen("0.0.0.0",stoi(cfg.get("listenport")));

    return 0;
}