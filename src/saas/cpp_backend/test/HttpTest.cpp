#include "../Http/httplib.h"
#include "../JsonCpp/json.hpp"
#include <iostream>

using namespace httplib;
using namespace std;
using json=nlohmann::json;

int main()
{
    Server server;

    json j1;

    // 数字 存储为 double
    j1["pi"] = 3.141;
    // Boolean 存储为 bool
    j1["happy"] = true;
    // 加入一个  array 存储为 std::vector (使用初始化列表)
    j1["list"] = { 1, 0, 2 };
    // 添加其他对象 (使用键值对初始化列表)
    j1["object"] = { {"currency", "USD"}, {"value", 42.99} };

    string j1str=j1.dump(); ///<序列化

    server.Get("/test",[](const Request &, Response& res){
        res.set_content("Hello World","text/plain");
    });

    server.Get("/tt",[](const Request &, Response& res){
        res.set_content("Hello tt","text/plain");
    });

    server.Get("/tjson",[&](const Request& ,Response& res){
        res.set_content(j1str,"text/json");
    });

    server.listen("0.0.0.0",8085);
    return 0;
}