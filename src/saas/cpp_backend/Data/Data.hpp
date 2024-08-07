#ifndef __DATA_HPP
#define __DATA_HPP

#include <iostream>
#include <memory>
#include <exception>
#include <sstream>

#include "../MysqlCpp/mysql.hpp"
#define FMT_HEADER_ONLY 
#include "../Fmt/core.h"

bool operator==(const std::string & s1,const char* s2)
{
    if(s1.size()!=strlen(s2)) return false;
    for(int i=0;i<s1.size();i++){
        if(tolower(s1[i])!=tolower(s2[i])) return false; 
    }
    return true;       
}

/**
 * @brief sql解析类 将json数据变成sql语句
 */
class Sql
{
public:
    static Sql* GetInstance()
    {
        static Sql sql;
        return &sql;
    }

    std::string to_string(json& j)
    {
        try{
            std::string action=j["action"].get<std::string>();
            m_table_name=j["table_name"].get<std::string>();
            j.erase("action");
            j.erase("table_name");
            if(action=="insert"){
                return insert_(j);
            }else if(action=="delete"){
                return delete_(j);
            }else if(action=="update"){
                return update_(j);
            }else if(action=="select"){
                return select_(j);
            }else{
                throw std::invalid_argument("Invalid action: "+action);
            }
            return "";
        }catch(std::exception& e){
            fprintf(stderr,"%s\n",e.what());
            return "";
        }
    }

protected:
    std::string insert_(const json& j)
    {
        std::stringstream pre,suf;
        pre<<"(";
        suf<<"(";
        bool first=true;
        for(auto& entry: j.items()){
            if(!first){
                pre<<", ";
                suf<<", ";
            }
            pre<<entry.key();
            if(json::value_t::string==entry.value().type()){
                suf<<"'"<<entry.value().get<std::string>()<<"'";
            }else suf<<entry.value().dump();
            first=false;
        }
        pre<<")";
        suf<<")";
        return fmt::format("insert into {} {} values {}",m_table_name,pre.str(),suf.str());
    }

    std::string delete_(const json& j)
    {
        if(j["condition"].is_null()){
            return fmt::format("delete from {}",m_table_name);
        }
        json con_j=j["condition"].get<json>();
        bool first=true;
        std::stringstream con;
        for(auto& entry: con_j.items()){
            if(!first) con<<" AND ";
            if(json::value_t::string==entry.value().type()){
                con<<fmt::format("{} = '{}'",entry.key(),entry.value().get<std::string>());
            }else{
                con<<fmt::format("{} = {}",entry.key(),entry.value().dump());
            }
            first=false;
        }
        return fmt::format("delete from {} where {}",m_table_name,con.str());
    }

    std::string update_(const json& j)
    {
        std::stringstream str,con;
        bool str_first=true,has_con=false;
        for(auto& entry: j.items()){
            if(entry.key()=="condition"){
                if(entry.value().is_null()) continue;
                has_con=true;
                json con_j=j["condition"].get<json>();
                bool first=true;
                for(auto& e: con_j.items()){
                    if(!first) con<<" AND ";
                    if(json::value_t::string==e.value().type()){
                        con<<fmt::format("{} = '{}'",e.key(),e.value().get<std::string>());
                    }else{
                        con<<fmt::format("{} = {}",e.key(),e.value().dump());
                    }
                    first=false;
                }
            }else{
                if(!str_first){
                    str<<", ";
                }
                str<<entry.key();
                str<<" = ";
                if(json::value_t::string==entry.value().type()){
                    str<<"'"<<entry.value().get<std::string>()<<"'";
                }else{
                    str<<entry.value().dump();
                }
                str_first=false;
            }
        }
        if(has_con){
            return fmt::format("update {} set {} where {}",m_table_name,str.str(),con.str());
        }
        return fmt::format("update {} set {}",m_table_name,str.str());
    }

    std::string select_(const json& j)
    {
        std::stringstream cols,con,order;
        int number=-1;
        bool has_cols=false,has_con=false,has_order=false,has_limit=false;
        for(auto& entry: j.items()){
            if(entry.key()=="cols"){
                if(entry.value().is_null()) continue;
                auto col=j["cols"].get<std::vector<std::string>>();
                if(col.empty()) continue;
                has_cols=true;
                bool first=true;
                for(auto& s: col){
                    if(!first) cols<<", ";
                    cols<<s;
                    first=false;
                }
            }else if(entry.key()=="condition"){
                if(entry.value().is_null()) continue;
                has_con=true;
                json con_j=j["condition"].get<json>();
                bool first=true;
                for(auto& e: con_j.items()){
                    if(!first) con<<" AND ";
                    if(json::value_t::string==e.value().type()){
                        con<<fmt::format("{} = '{}'",e.key(),e.value().get<std::string>());
                    }else{
                        con<<fmt::format("{} = {}",e.key(),e.value().dump());
                    }
                    first=false;
                }
            }else if(entry.key()=="order"){
                if(entry.value().is_null()) continue;
                has_order=true;
                json order_j=j["order"].get<json>();
                if(order_j["column_name"].is_null()){
                    has_order=false;
                    continue;
                }
                order<<order_j["column_name"].get<std::string>();
                if(!order_j["end"].is_null()) order<<" "<<order_j["end"].get<std::string>();
            }else if(entry.key()=="limit"){
                if(entry.value().is_null()) continue;
                has_limit=true;
                number=j["limit"].get<std::size_t>();
            }
        }
        std::stringstream ans;
        ans<<"select ";
        if(has_cols) ans<<cols.str()<<" ";
        else ans<<"* ";
        ans<<"from "<<m_table_name<<" ";
        if(has_con) ans<<"where "<<con.str()<<" ";
        if(has_order) ans<<"order by "<<order.str()<<" ";
        if(number>0) ans<<"limit "<<number;
        return ans.str();
    }

private:
    std::string m_table_name;

    Sql()=default;
    Sql(const Sql& sql)=default;
    Sql& operator=(const Sql& sql)=default;
    Sql(Sql&& sql)=default;
    Sql& operator=(Sql&& sql)=default;
};

#define SQL_PARSE(j) Sql::GetInstance()->to_string(j)

namespace data
{
    enum{
        SQL_FAIL=500,
        JSON_FAIL=501
    };
    class BasicData
    {
    public:
        BasicData(const std::string& url,const std::string& user,const std::string& password,const std::string& databasename)
        :m_mysql(url,user,password,databasename)
        {
        }
        virtual ~BasicData(){}

        int Execute(const json& req,json& res)
        {
            return execute_(std::move(req),res);
        }

        int Execute(json& req,json& res)
        {
            return execute_(req,res);
        }

    protected:
        virtual int execute_(const json& req,json& res){}
        virtual int execute_(json& req,json& res){}

        Mysql m_mysql;
    private:
        std::string m_url;
        std::string m_user;
        std::string m_password;
        std::string m_databasename;
    };

    class Login: public BasicData
    {   
        enum{
            LOGIN_SUCCESS=200,
            LOGIN_FAIL=400
        };
    public:
        Login(const std::string& url,const std::string& user,const std::string& password,const std::string& databasename)
        :BasicData(url,user,password,databasename)
        {            
        }

        int execute_(const json& req,json& res) override
        {
            //fmt::print("{}\n",1);
            res.clear();
            bool check=false;
            int n;
            res["state"]=LOGIN_FAIL;
            res["message"]="登录失败";
            std::cout<<req<<std::endl;
            try{
                std::string acc=req.at("userAcc").get<std::string>();
                std::string pwd=req.at("userPwd").get<std::string>();
                json mysql_res;
                n=m_mysql.Query(fmt::format("SELECT * FROM user_accounts WHERE user_id={}",acc),mysql_res);
                //std::cout<<mysql_res[0].at("password").get<std::string>()<<std::endl;
                check=pwd==mysql_res[0].at("password").get<std::string>();
            }catch(std::exception &e){
                fprintf(stderr,"执行错误\n");
            }
            if(check){
                res["state"]=LOGIN_SUCCESS;
                res["message"]="登录成功";
            }
            return n;
        }

    };

    class SignUp:public BasicData
    {
        enum{
            SIGNUP_SUCCESS=200,
            SIGNUP_EXIST=402,
            SIGNUP_EMPTY=403,
        };
    public:
        SignUp(const std::string& url,const std::string& user,const std::string& password,const std::string& databasename)
        :BasicData(url,user,password,databasename)
        {            
        }

        int execute_(const json& req,json& res) override
        {
            res.clear();
            int n;
            res["state"]=SIGNUP_SUCCESS;
            res["message"]="注册成功";
            try{
                std::string acc=req.at("Acc_sign").get<std::string>();
                std::string username=req.at("username").get<std::string>();
                std::string password=req.at("psw_sign").get<std::string>();
                std::string phone_number=req.at("phone_number").get<std::string>();
                //std::cout<<fmt::format("INSERT INTO VALUES({},'{}','{}','{}')",acc,username,password,phone_number)<<std::endl;
                n=m_mysql.Query(fmt::format("INSERT INTO user_accounts(user_id,username,password,phone_number) VALUES({},'{}','{}','{}')",acc,username,password,phone_number));
            }catch(std::exception& e){
                fprintf(stderr,"执行错误\n");
                res["state"]=SIGNUP_EMPTY;
                res["message"]="参数错误 或 解析错误";
                return n;
            }
            if(n){
                if(1062==n){
                    res["state"]=SIGNUP_EXIST;
                    res["message"]="用户已存在";
                }else{
                    res["state"]=SQL_FAIL;
                    res["errno"]=n;
                    res["message"]="执行语句错误";
                }
            }
            return n;
        }

    };

    class DownloadWaterData: public BasicData
    {
        enum{
            DownloadWaterData_SUCCESS=200,
            DownloadWaterData_NOEXIST=404
        };
    public:
        DownloadWaterData(const std::string& url,const std::string& user,const std::string& password,const std::string& databasename)
        :BasicData(url,user,password,databasename)
        {
        }

        int execute_(const json& req,json& res) override
        {
            res.clear();
            int n;
            res["state"]=DownloadWaterData_SUCCESS;
            res["message"]="下载成功";
            try{
                std::string id=req.at("water_data_id").get<std::string>();
                json mysql_res;
                n=m_mysql.Query(fmt::format("SELECT * FROM water_quality_data WHERE water_data_id={}",id),mysql_res);
                if(mysql_res.empty()){
                    res["state"]=DownloadWaterData_NOEXIST;
                    res["message"]="下载失败";
                    return n;
                }
                res["obj"]=mysql_res[0];
            }catch(std::exception& e){
                fprintf(stderr,"执行错误\n");
                res["state"]=JSON_FAIL;
                res["message"]="参数错误 或 解析错误";
                return n;
            }
        }
    };

    class ShowWaterData:public BasicData
    {
        enum{
            ShowWaterData_SUCCESS=200,
            ShowWaterData_ERROR=400,
            ShowWaterData_NOEXIST=404
        };
    public:
        ShowWaterData(const std::string& url,const std::string& user,const std::string& password,const std::string& databasename)
        :BasicData(url,user,password,databasename)
        {
        }

        int execute_(const json& req,json& res) override
        {
            res.clear();
            json mysql_res;
            int n=m_mysql.Query(fmt::format("SELECT * FROM water_quality_data"),mysql_res);
            if(mysql_res.empty()){
                res["state"]=ShowWaterData_NOEXIST;
                res["message"]="未找到";
            }else if(n){
                res["state"]=ShowWaterData_ERROR;
                res["message"]="参数错误";
            }else{
                res["state"]=ShowWaterData_SUCCESS;
                res["message"]="展示数据获取成功";
                res["excel"]=mysql_res;
            }
            return n;
        }
    };

    class OperatorMysql: public BasicData
    {
    public:
        OperatorMysql(const std::string& url,const std::string& user,const std::string& password,const std::string& databasename)
        :BasicData(url,user,password,databasename)
        {
        }

        int execute_(json& req,json& res) override
        {
            res.clear();
            json mysql_res;
            //std::cout<<SQL_PARSE(req)<<std::endl;
            int n=m_mysql.Query(SQL_PARSE(req),mysql_res);
            if(n){
                res["message"]="操作失败";
            }else{
                res["message"]="操作成功";
            } 
            res["errno"]=n;
            res["return"]=mysql_res;
            return n;
        }
    };
}

#endif