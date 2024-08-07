#ifndef __MYSQL_HPP
#define __MYSQL_HPP

#include <iostream>
#include <mysql/mysql.h>

#include "../JsonCpp/json.hpp"
using json=nlohmann::json;

class Mysql
{
public:
    Mysql(){}

    Mysql(const std::string& url,const std::string& user,const std::string& password,const std::string& databasename)
    :m_url(url),m_user(user),m_password(password),m_databasename(databasename)
    {
        mysql_init(&m_conn);
        if(mysql_real_connect(&m_conn,m_url.c_str(),m_user.c_str(),m_password.c_str(),m_databasename.c_str(),0,nullptr,0)==NULL){
            fprintf(stderr,"mysql connect failed\n");
            mysql_close(&m_conn);
            exit(-1);
        }
        mysql_set_character_set(&m_conn,"utf8mb4");
    }

    /**
     * @brief 执行sql语句,只看成功与否
     * @param sql 执行的sql语句
     * @return 0成功 其余错误码
     */
    int Query(const std::string& sql)
    {
        int res=mysql_query(&m_conn,sql.c_str());
        if(res){
            res=mysql_errno(&m_conn);
        }
        return res;
    }

    /**
     * @brief 执行sql语句
     * @param slq 执行的sql语句
     * @param j 返回的json数据
     * @return 0 成功 其余错误码
     */
    int Query(const std::string& sql,json& j)
    {
        int n=mysql_query(&m_conn,sql.c_str());
        j.clear();
        if(n){
            n=mysql_errno(&m_conn);
            return n;
        }
        MYSQL_RES* res=mysql_store_result(&m_conn);
        if(res==nullptr){
            fprintf(stdout,"return datas is empty\n");
            return n;
        }
        int rows=mysql_num_rows(res);
        int cols=mysql_num_fields(res);
        MYSQL_FIELD* col_name=mysql_fetch_field(res);
        for(int i=0;i<rows;i++){
            line=mysql_fetch_row(res);
            json tmp;
            for(int j=0;j<cols;j++){
                if(line[j]==NULL) line[j]="";
                tmp[col_name[j].name]=line[j];
            }
            j.push_back(std::move(tmp));
        }
        std::cout<<j<<std::endl;
        return n;
    }

    ~Mysql()
    {
        mysql_close(&m_conn);
        fprintf(stdout,"mysql connect close\n");
    }
private:
    MYSQL m_conn;
    MYSQL_ROW line;
    std::string m_url;
    std::string m_user;
    std::string m_password;
    std::string m_databasename;
};

#endif