#include <cstdint>
#include <iostream>

#include "napi/native_api.h"
#include "json.hpp"
#include "mavlink.h"
#include "hilog/log.h"
#include "encode.hpp"
#include "decode.hpp"

using json=nlohmann::json;

static napi_value Add(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args , nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    napi_valuetype valuetype1;
    napi_typeof(env, args[1], &valuetype1);

    double value0;
    napi_get_value_double(env, args[0], &value0);

    double value1;
    napi_get_value_double(env, args[1], &value1);

    napi_value sum;
    napi_create_double(env, value0 + value1, &sum);
    
    json j=R"({"mav_cmd":76,"target_system":1,"target_component":1,"command":2,"confirmation":3,"param1":1.0,"param2":2,"param3":3,"param4":4.0,"param5":0,"param6":6.45,"param7":7.7})";
    MavLink_Pack_t pack=Encode(j);
    json jj;
    std::string tt="123";
    std::uint16_t u16[8]={23,46};
    jj["tt"]=tt;
    jj["u16"]=u16;
    OH_LOG_Print(LOG_APP, LOG_DEBUG, 0X2005, "INFO_TAG", "%{public}d",36);
    OH_LOG_Print(LOG_APP, LOG_DEBUG, 0X2005, "INFO_TAG", "%{public}d",pack->buffer_[0]);
    OH_LOG_Print(LOG_APP, LOG_DEBUG, 0X2005, "INFO_TAG", "%{public}s",jj.dump().c_str());
    
    return sum;
}

static napi_value JsonTo32Hex(napi_env env, napi_callback_info info)
{
    size_t argc=2;
    napi_value args[2]={nullptr};
    napi_get_cb_info(env,info, &argc, args, nullptr, nullptr);
    
    char buf[300];
    napi_get_value_string_utf8(env,args[0],buf,300, nullptr);
    OH_LOG_Print(LOG_APP, LOG_INFO, 0x2000,"TAG_APP","%{public}s", buf);
    
    MavLink_Pack_t pack=Encode(buf);
    
    //处理->变成js类型->uin32
    napi_value value;
    napi_create_array_with_length(env, pack->buflen_, &value);
    for(int i=0;i<pack->buflen_;i++){
        napi_value one;
        napi_create_int32(env, pack->buffer_[i], &one);
        napi_set_element(env, value, i, one);
    }
    
    return value;
}

//会有问题 TODO
static napi_value JsonTo8Hex(napi_env env, napi_callback_info info)
{
    size_t argc=2;
    napi_value args[2]={nullptr};
    napi_get_cb_info(env,info, &argc, args, nullptr, nullptr);
    
    char buf[300];
    napi_get_value_string_utf8(env,args[0],buf,300, nullptr);
    OH_LOG_Print(LOG_APP, LOG_INFO, 0x2000,"TAG_APP","%{public}s", buf);
    
    MavLink_Pack_t pack=Encode(buf);
    
    //处理->变成js类型->uin8->string
    napi_value value;
    napi_create_string_utf8(env, (char*)pack->buffer_,pack->buflen_, &value);
    
    return value;
}

static napi_value _8HexToJson(napi_env env,napi_callback_info info)
{
    size_t argc=2;
    napi_value args[2]={nullptr};
    napi_get_cb_info(env,info, &argc, args, nullptr, nullptr);
    
    void* buffer=nullptr;
    size_t buflen;
    
    napi_get_arraybuffer_info(env, args[0], &buffer, &buflen);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack((std::uint8_t*)buffer,buflen));
    //free(buffer);
    
    //解码成json序列化后的字符串
    std::string str=Decode(pack);
    
    //将字符串变成napi_value
    napi_value value;
    napi_create_string_utf8(env, str.c_str(), str.size(), &value);
    
    return value;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        { "add", nullptr, Add, nullptr, nullptr, nullptr, napi_default, nullptr },         
        { "JsonTo32Hex", nullptr, JsonTo32Hex, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "JsonTo8Hex", nullptr, JsonTo8Hex, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "_8HexToJson", nullptr,_8HexToJson, nullptr, nullptr, nullptr, napi_default, nullptr },
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END

static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "entry",
    .nm_priv = ((void*)0),
    .reserved = { 0 },
};

extern "C" __attribute__((constructor)) void RegisterEntryModule(void)
{
    napi_module_register(&demoModule);
}
