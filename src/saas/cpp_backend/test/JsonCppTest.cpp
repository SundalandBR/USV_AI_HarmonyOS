#include <iostream>

#include "../JsonCpp/json.hpp"
using json=nlohmann::json;
using namespace std;

#define print(a) cout<<(a)<<endl

int main()
{
    json t;
    t=R"({"name":null,"ttt":123})"_json;
    print(t);
    for(auto& e: t.items()){
        cout<<e.key()<<endl;
    }
    print(t.at("name"));
    print(t.at("name").is_null());
    return 0;
}