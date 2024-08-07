#pragma once

#include <iostream>

#include "json.hpp"
#include "hilog/log.h"

//mavlink消息枚举类型
enum MAVLINK_MSG_ID{
    HEARTBEAT=0,
    SET_MODE=11,
    PARAM_REQUEST_LIST=21,
    PARAM_VALUE=22,
    GPS_RAW_INT=24,
    ATTITUDE=30,
    MISSION_WRITE_PARTIAL_LIST=38,
    MISSION_ITEM=39,
    MISSION_REQUEST=40,
    MISSION_SET_CURRENT=41,
    MISSION_REQUEST_LIST=43,
    MISSION_COUNT=44,
    MISSION_CLEAR_ALL=45,
    MISSION_ACK=47,
    MISSION_REQUEST_INT=51,
    REQUEST_DATA_STREAM=66,
    MISSION_ITEM_INT=73,
    VFR_HUD=74,
    COMMAND_LONG=76,
    BATTERY_STATUS=147,
};

/**
 * @brief 封装了返回值，是地址和长度
 * */
struct MavLink_Pack
{
    explicit MavLink_Pack(std::size_t bufsize=0)
    {
        if(bufsize<=0) bufsize=1;
        buffer_=new std::uint8_t[bufsize];
        buflen_=bufsize;
    }

    explicit MavLink_Pack(std::uint8_t* buffer,std::size_t buflen)
    {
        if(buffer==NULL) return ;
        delete [] buffer_;
        buffer_=NULL;
        buffer_=new std::uint8_t[buflen];
        buflen_=buflen;
        memcpy(buffer_, buffer, buflen);
    }
    
    MavLink_Pack(const MavLink_Pack& rhs)
    {
        delete [] buffer_;
        buffer_=NULL;
        buflen_=rhs.buflen_;
        buffer_=new std::uint8_t[rhs.buflen_];
        memcpy(buffer_,rhs.buffer_,rhs.buflen_);
    }
    
    MavLink_Pack& operator=(const MavLink_Pack& rhs)
    {
        if(&rhs==this) return *this;
        delete [] buffer_;
        buffer_=NULL;
        buflen_=rhs.buflen_;
        buffer_=new std::uint8_t[rhs.buflen_];
        memcpy(buffer_,rhs.buffer_,rhs.buflen_);
        return *this;
    }
    
    MavLink_Pack(MavLink_Pack&& rhs)
    {
        delete [] buffer_;
        buffer_=NULL;
        buflen_=rhs.buflen_;
        buffer_=rhs.buffer_;
        rhs.buffer_=nullptr;
    }
    
    MavLink_Pack& operator=(MavLink_Pack&& rhs)
    {
        if(this==&rhs) return *this;
        delete [] buffer_;
        buffer_=NULL;
        buflen_=rhs.buflen_;
        buffer_=rhs.buffer_;
        rhs.buffer_=nullptr;
        return *this;
    }
    
    ~MavLink_Pack()
    {
        //OH_LOG_Print(LOG_APP, LOG_DEBUG, 0X2005, "INFO_TAG", "%{public}s","准备释放");
        delete [] buffer_;
        buffer_=NULL;
        //OH_LOG_Print(LOG_APP, LOG_DEBUG, 0X2005, "INFO_TAG", "%{public}s","被释放了");
    }
    
    std::size_t buflen_;
    std::uint8_t* buffer_=NULL;
};

std::ostream& operator<<(std::ostream& os,const MavLink_Pack& pack)
{
    for(int i=0;i<pack.buflen_;i++){
        os<<"buffer["<<i<<"] = "<<pack.buffer_[i]<<" ";
    }
    os<<std::endl;
    return os;
}

typedef std::shared_ptr<MavLink_Pack> MavLink_Pack_t;