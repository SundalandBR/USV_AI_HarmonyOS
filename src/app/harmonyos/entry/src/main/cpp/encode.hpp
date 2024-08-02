//
// Created on 2024/7/27.
//
// Node APIs are not fully supported. To solve the compilation error of the interface cannot be found,
// please include "napi/native_api.h".
#pragma once

#include "mavlink.h"
#include "mavlink_msg_command_long.h"
#include "mavlink_msg_mission_ack.h"
#include "mavlink_msg_mission_clear_all.h"
#include "mavlink_msg_mission_count.h"
#include "mavlink_msg_mission_item.h"
#include "mavlink_msg_mission_request_int.h"
#include "mavlink_msg_mission_request_list.h"
#include "mavlink_msg_mission_set_current.h"
#include "mavlink_msg_mission_write_partial_list.h"
#include "mavlink_msg_param_request_list.h"
#include "mavlink_msg_param_value.h"
#include "mavlink_msg_request_data_stream.h"
#include "mavlink_msg_set_mode.h"

#include "common.hpp"
#include "minimal/mavlink_msg_heartbeat.h"

using json=nlohmann::json;

const std::uint8_t system_id=1;
const std::uint8_t component_id=1;

void from_json(const json& j,mavlink_command_long_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.command=j["command"].get<std::uint16_t>();
        value.confirmation=j["confirmation"].get<std::uint8_t>();
        value.param1=j["param1"].get<std::float_t>();
        value.param2=j["param2"].get<std::float_t>();
        value.param3=j["param3"].get<std::float_t>();
        value.param4=j["param4"].get<std::float_t>();
        value.param5=j["param5"].get<std::float_t>();
        value.param6=j["param6"].get<std::float_t>();
        value.param7=j["param7"].get<std::float_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeCommandLong(const json& j)
{
    mavlink_message_t msg;
    mavlink_command_long_t value;
    
    from_json(j, value);
    
    mavlink_msg_command_long_encode(system_id, component_id,&msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_,&msg);
    
    return pack;
}

void from_json(const json& j,mavlink_param_value_t& value)
{
    try{
        std::string param_id=j["param_id"].get<std::string>();
        memcpy(value.param_id,param_id.c_str(),std::min(param_id.size()+1,(std::size_t)16));
        value.param_value=j["param_value"].get<std::float_t>();
        value.param_type=j["param_type"].get<std::uint8_t>();
        value.param_count=j["param_count"].get<std::uint16_t>();
        value.param_index=j["param_index"].get<std::uint16_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeParamValue(const json& j)
{
    mavlink_message_t msg;
    mavlink_param_value_t value;
    
    from_json(j, value);
    
    mavlink_msg_param_value_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_param_request_list_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeParamRequestList(const json& j)
{
    mavlink_message_t msg;
    mavlink_param_request_list_t value;
    
    from_json(j, value);
    
    mavlink_msg_param_request_list_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_request_data_stream_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.req_stream_id=j["req_stream_id"].get<std::uint8_t>();
        value.req_message_rate=j["req_message_rate"].get<std::uint16_t>();
        value.start_stop=j["start_stop"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeRequestDataStream(const json& j)
{
    mavlink_message_t msg;
    mavlink_request_data_stream_t value;
    
    from_json(j, value);
    
    mavlink_msg_request_data_stream_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_set_mode_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.base_mode=j["base_mode"].get<std::uint8_t>();
        value.custom_mode=j["custom_mode"].get<std::uint32_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeSetMode(const json& j)
{
    mavlink_message_t msg;
    mavlink_set_mode_t value;
    
    from_json(j, value);
    
    mavlink_msg_set_mode_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_write_partial_list_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.start_index=j["start_index"].get<std::uint16_t>();
        value.end_index=j["end_index"].get<std::uint16_t>();
        value.mission_type=j["mission_type"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionWritePartialList(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_write_partial_list_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_write_partial_list_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_request_list_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.mission_type=j["mission_type"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionRequestList(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_request_list_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_request_list_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_count_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.count=j["count"].get<std::uint16_t>();
        value.mission_type=j["mission_type"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionCount(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_count_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_count_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_clear_all_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.mission_type=j["mission_type"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionClearAll(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_clear_all_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_clear_all_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_item_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.seq=j["seq"].get<std::uint16_t>();
        value.frame=j["frame"].get<std::uint8_t>();
        value.command=j["command"].get<std::uint16_t>();
        value.current=j["current"].get<std::uint8_t>();
        value.autocontinue=j["autocontinue"].get<std::uint8_t>();
        value.param1=j["param1"].get<std::float_t>();
        value.param2=j["param2"].get<std::float_t>();
        value.param3=j["param3"].get<std::float_t>();
        value.param4=j["param4"].get<std::float_t>();
        value.x=j["x"].get<std::float_t>();
        value.y=j["y"].get<std::float_t>();
        value.z=j["z"].get<std::float_t>();
        value.mission_type=j["mission_type"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionItem(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_item_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_item_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_item_int_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.seq=j["seq"].get<std::uint16_t>();
        value.frame=j["frame"].get<std::uint8_t>();
        value.command=j["command"].get<std::uint16_t>();
        value.current=j["current"].get<std::uint8_t>();
        value.autocontinue=j["autocontinue"].get<std::uint8_t>();
        value.param1=j["param1"].get<std::float_t>();
        value.param2=j["param2"].get<std::float_t>();
        value.param3=j["param3"].get<std::float_t>();
        value.param4=j["param4"].get<std::float_t>();
        value.x=j["x"].get<std::float_t>();
        value.y=j["y"].get<std::float_t>();
        value.z=j["z"].get<std::float_t>();
        value.mission_type=j["mission_type"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionItemInt(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_item_int_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_item_int_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_request_int_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.seq=j["seq"].get<std::uint16_t>();
        value.mission_type=j["mission_type"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionRequestInt(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_request_int_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_request_int_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_request_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.seq=j["seq"].get<std::uint16_t>();
        value.mission_type=j["mission_type"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionRequest(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_request_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_request_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_ack_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.type=j["type"].get<std::uint8_t>();
        value.mission_type=j["mission_type"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionAck(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_ack_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_ack_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_mission_set_current_t& value)
{
    try{
        value.target_system=j["target_system"].get<std::uint8_t>();
        value.target_component=j["target_component"].get<std::uint8_t>();
        value.seq=j["seq"].get<std::uint16_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeMissionSetCurrent(const json& j)
{
    mavlink_message_t msg;
    mavlink_mission_set_current_t value;
    
    from_json(j, value);
    
    mavlink_msg_mission_set_current_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

void from_json(const json& j,mavlink_heartbeat_t& value)
{
    try{
        value.type=j["type"].get<std::uint8_t>();
        value.autopilot=j["autopilot"].get<std::uint8_t>();
        value.base_mode=j["base_mode"].get<std::uint8_t>();
        value.custom_mode=j["custom_mode"].get<std::uint32_t>();
        value.system_status=j["system_status"].get<std::uint8_t>();
        value.mavlink_version=j["mavlink_version"].get<std::uint8_t>();
    }catch(std::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
    }
}

MavLink_Pack_t EncodeHeartbeat(const json& j)
{
    mavlink_message_t msg;
    mavlink_heartbeat_t value;
    
    from_json(j, value);
    
    mavlink_msg_heartbeat_encode(system_id,component_id, &msg, &value);
    
    MavLink_Pack_t pack=MavLink_Pack_t(new MavLink_Pack(512));
    pack->buflen_=mavlink_msg_to_send_buffer(pack->buffer_, &msg);
    
    return pack;
}

MavLink_Pack_t Encode(const std::string& str)
{   
    OH_LOG_Print(LOG_APP, LOG_INFO, 0X2005, "INFO_TAG", "%{public}s",str.c_str());
    MavLink_Pack_t pack=nullptr;
    try{
        json j=json::parse(str);
        std::size_t mav_cmd=j["mav_cmd"].get<std::size_t>();
        switch(mav_cmd){
            case MAVLINK_MSG_ID::HEARTBEAT:
                pack=EncodeHeartbeat(j);
                break;
            case MAVLINK_MSG_ID::MISSION_SET_CURRENT:
                pack=EncodeMissionSetCurrent(j);
                break;
            case MAVLINK_MSG_ID::MISSION_ACK:
                pack=EncodeMissionAck(j);
                break;
            case MAVLINK_MSG_ID::MISSION_REQUEST:
                pack=EncodeMissionRequest(j);
                break;
            case MAVLINK_MSG_ID::MISSION_REQUEST_INT:
                pack=EncodeMissionRequestInt(j);
                break;
            case MAVLINK_MSG_ID::MISSION_ITEM_INT:
                pack=EncodeMissionItemInt(j);
                break;
            case MAVLINK_MSG_ID::MISSION_ITEM:
                pack=EncodeMissionItem(j);
                break;
            case MAVLINK_MSG_ID::MISSION_CLEAR_ALL:
                pack=EncodeMissionClearAll(j);
                break;
            case MAVLINK_MSG_ID::MISSION_COUNT:
                pack=EncodeMissionCount(j);
                break;
            case MAVLINK_MSG_ID::MISSION_REQUEST_LIST:
                pack=EncodeMissionRequestList(j);
                break;
            case MAVLINK_MSG_ID::MISSION_WRITE_PARTIAL_LIST:
                pack=EncodeMissionWritePartialList(j);
                break;
            case MAVLINK_MSG_ID::SET_MODE:
                pack=EncodeSetMode(j);
                break;
            case MAVLINK_MSG_ID::REQUEST_DATA_STREAM:
                pack=EncodeRequestDataStream(j);
                break;
            case MAVLINK_MSG_ID::PARAM_REQUEST_LIST:
                pack=EncodeParamRequestList(j);
                break;
            case MAVLINK_MSG_ID::COMMAND_LONG:
                pack=EncodeCommandLong(j);
                break;
            case MAVLINK_MSG_ID::PARAM_VALUE:
                pack=EncodeParamValue(j);
                break;
            default:
                pack=MavLink_Pack_t(new MavLink_Pack(1));
                pack->buffer_[0]=-1;
                break;
        }
    }catch(json::exception& e){
        OH_LOG_Print(LOG_APP, LOG_ERROR, 0X2005, "ERROR_TAG","%{public}s",e.what());
        pack=MavLink_Pack_t(new MavLink_Pack(1));
        pack->buffer_[0]=-1;
    }
    OH_LOG_Print(LOG_APP, LOG_DEBUG, 0X2005, "INFO_TAG", "buflen = %{public}d",pack->buflen_);
    for(int i=0;i<pack->buflen_;i++){
        OH_LOG_Print(LOG_APP, LOG_DEBUG, 0X2005, "INFO_TAG", "buffer[%{public}d] = %{public}d",i,pack->buffer_[i]);
    }
    return pack;
}