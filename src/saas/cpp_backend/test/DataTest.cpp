#include <iostream>

#include "../Data/Data.hpp"

using namespace std;
using namespace data;

#define print(a) cout<<(a)<<endl;

int main()
{
#if 0
    BasicData* data=new Login("47.96.237.24","root","Qwe123456789...++","qianduoduo");
    json j;
    data->Execute({{"userAcc","123"},{"userPwd","456"}},j);
    std::cout<<j<<std::endl;
    data->Execute({{"userAcc","8888888"},{"userPwd","111111"}},j);
    std::cout<<j<<std::endl;
    data->Execute({{"userAc","8888888"},{"userPwd","111111"}},j);
    std::cout<<j<<std::endl;
    data->Execute({{"userAcc","8888888"},{"userPwd","1111"}},j);
    std::cout<<j<<std::endl;
    data->Execute({{"userAcc","1069366295"},{"userPwd","qwe123"}},j);
    std::cout<<j<<std::endl;
    delete data;
#endif

#if 1
    BasicData* data=new SignUp("47.96.237.24","root","Qwe123456789...++","qianduoduo");
    json j;
    data->Execute({{"Acc_sign","11"},{"psw_sign","333"},{"phone_number","333"}},j);
    print(j);
    data->Execute({{"Acc_sign","8888888"},{"username","22"},{"psw_sign","333"},{"phone_number","333"}},j);
    print(j);
    data->Execute({{"Acc_sign","13579"},{"username","2468"},{"psw_sign","996"},{"phone_number","12345678"}},j);
    print(j);
    delete data;
#endif
    return 0;
}