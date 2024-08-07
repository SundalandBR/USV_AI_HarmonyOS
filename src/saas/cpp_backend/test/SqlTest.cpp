#include <iostream>

#include "../Data/Data.hpp"

using namespace std;

int main()
{   
    json j1=R"({"action":"insert","table_name":"user","user_id":123,"user_name":"12345"})"_json;
    cout<<SQL_PARSE(j1)<<endl;
    json j2=R"({"action":"delete","table_name":"user","condition":{"user_id":124,"user_name":"123"}})"_json;
    cout<<SQL_PARSE(j2)<<endl;
    json j3=R"({"action":"update","table_name":"user","user_name":"1234","condition":{"user_id":123}})"_json;
    cout<<SQL_PARSE(j3)<<endl;
    json j4=R"({"action":"select","table_name":"user","cols":["user_id","user_name"],"order":{"column_name":"user_id","end":"desc"},"limit":100})"_json;
    cout<<SQL_PARSE(j4)<<endl;
    return 0;
}