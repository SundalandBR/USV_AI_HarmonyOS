#pragma once

#include "common.hpp"
#include "mavlink.h"
#include "mavlink_helpers.h"
#include "mavlink_msg_attitude.h"
#include "mavlink_msg_battery_status.h"
#include "mavlink_msg_gps_raw_int.h"
#include "mavlink_msg_param_request_list.h"
#include "mavlink_msg_vfr_hud.h"
#include "mavlink_types.h"
#include "minimal/mavlink_msg_heartbeat.h"

using json=nlohmann::json;

void to_json(const mavlink_heartbeat_t& value,json& j)
{
    j["mav_cmd"]=MAVLINK_MSG_ID::HEARTBEAT;
    
    j["type"]=value.type;
    j["autopilot"]=value.autopilot;
    j["base_mode"]=value.base_mode;
    j["custom_mode"]=value.custom_mode;
    j["system_status"]=value.system_status;
    j["mavlink_version"]=value.mavlink_version;
}

std::string DecodeHeartbeat(const mavlink_message_t& msg)
{
    mavlink_heartbeat_t value;
    
    mavlink_msg_heartbeat_decode(&msg, &value);
    
    json j;
    to_json(value, j);
    
    return j.dump();
}

void to_json(const mavlink_param_request_list_t& value,json& j)
{
    j["mav_cmd"]=MAVLINK_MSG_ID::PARAM_REQUEST_LIST;
    
    j["target_system"]=value.target_system;
    j["target_component"]=value.target_component;
}

std::string DecodeParamRequestList(const mavlink_message_t& msg)
{
    mavlink_param_request_list_t value;
    
    mavlink_msg_param_request_list_decode(&msg, &value);
    
    json j;
    to_json(value, j);
    
    return j.dump();
}

void to_json(const mavlink_attitude_t& value,json& j)
{
    j["mav_cmd"]=MAVLINK_MSG_ID::ATTITUDE;
    
    j["time_boot_ms"]=value.time_boot_ms;
    j["roll"]=value.roll;
    j["pitch"]=value.pitch;
    j["yaw"]=value.yaw;
    j["rollspeed"]=value.rollspeed;
    j["pitchspeed"]=value.pitchspeed;
    j["yawspeed"]=value.yawspeed;
}

std::string DecodeAttitude(const mavlink_message_t& msg)
{
    mavlink_attitude_t value;
    
    mavlink_msg_attitude_decode(&msg, &value);
    
    json j;
    to_json(value, j);
    
    return j.dump();
}

void to_json(const mavlink_gps_raw_int_t& value,json& j)
{
    j["mav_cmd"]=MAVLINK_MSG_ID::GPS_RAW_INT;
    
    j["time_usec"]=value.time_usec;
    j["fix_type"]=value.fix_type;
    j["lat"]=value.lat;
    j["lon"]=value.lon;
    j["alt"]=value.alt;
    j["eph"]=value.eph;
    j["epv"]=value.epv;
    j["vel"]=value.vel;
    j["con"]=value.cog;
    j["satellites_visible"]=value.satellites_visible;
    j["alt_ellipsoid"]=value.alt_ellipsoid;
    j["h_acc"]=value.h_acc;
    j["v_acc"]=value.v_acc;
    j["vel_acc"]=value.vel_acc;
    j["hdg_acc"]=value.hdg_acc;
    j["yaw"]=value.yaw;
}

std::string DecodeGpsRawInt(const mavlink_message_t& msg)
{
    mavlink_gps_raw_int_t value;
    
    mavlink_msg_gps_raw_int_decode(&msg, &value);
    
    json j;
    to_json(value, j);
    
    return j.dump();
}

void to_json(const mavlink_battery_status_t& value,json& j)
{
    j["mav_cmd"]=MAVLINK_MSG_ID::BATTERY_STATUS;
    
    j["id"]=value.id;
    j["battery_function"]=value.battery_function;
    j["type"]=value.type;
    j["temperature"]=value.temperature;
    j["voltages"]=value.voltages;
    j["current_battery"]=value.current_battery;
    j["current_consumed"]=value.current_consumed;
    j["energy_consumed"]=value.energy_consumed;
    j["battery_remaining"]=value.battery_remaining;
    j["time_remaining"]=value.time_remaining;
    j["charge_state"]=value.charge_state;
    j["voltages_ext"]=value.voltages_ext;
    j["mode"]=value.mode;
    j["fault_bitmask"]=value.fault_bitmask;
}

std::string DecodeBatteryStatus(const mavlink_message_t& msg)
{
    mavlink_battery_status_t value;
    
    mavlink_msg_battery_status_decode(&msg, &value);
    
    json j;
    to_json(value, j);
    
    return j.dump();
}

void to_json(const mavlink_vfr_hud_t& value,json& j)
{
    j["mav_cmd"]=MAVLINK_MSG_ID::VFR_HUD;
    
    j["airspeed"]=value.airspeed;
    j["groundspeed"]=value.groundspeed;
    j["heading"]=value.heading;
    j["throttle"]=value.throttle;
    j["alt"]=value.alt;
    j["climb"]=value.climb;
}

std::string DecodeVfrHud(const mavlink_message_t& msg)
{
    mavlink_vfr_hud_t value;
    
    mavlink_msg_vfr_hud_decode(&msg, &value);
    
    json j;
    to_json(value, j);
    
    return j.dump();
}

void to_json(const mavlink_mission_request_int_t &value, json &j) {
    j["mav_cmd"] = MAVLINK_MSG_ID::MISSION_REQUEST_INT;
    
    j["target_system"]=value.target_system;
    j["target_component"]=value.target_component;
    j["seq"]=value.seq;
    j["mission_type"]=value.mission_type;
}
std::string DecodeMissionRequestInt(const mavlink_message_t &msg) {
    mavlink_mission_request_int_t value;
    
    mavlink_msg_mission_request_int_decode(&msg, &value);
    
    json j;
    to_json(value, j);
    
    return j.dump();
}

void to_json(const mavlink_mission_request_t &value, json &j) {
    j["mav_cmd"] = MAVLINK_MSG_ID::MISSION_REQUEST;
    
    j["target_system"]=value.target_system;
    j["target_component"]=value.target_component;
    j["seq"]=value.seq;
    j["mission_type"]=value.mission_type;
}
std::string DecodeMissionRequest(const mavlink_message_t &msg) {
    mavlink_mission_request_t value;
    
    mavlink_msg_mission_request_decode(&msg, &value);
    
    json j;
    to_json(value, j);
    
    return j.dump();
}

void to_json(const mavlink_mission_ack_t &value, json &j) {
    j["mav_cmd"] = MAVLINK_MSG_ID::MISSION_ACK;
    
    j["target_system"]=value.target_system;
    j["target_component"]=value.target_component;
    j["type"]=value.type;
    j["mission_type"]=value.mission_type;
}
std::string DecodeMissionAck(const mavlink_message_t &msg) {
    mavlink_mission_ack_t value;
    
    mavlink_msg_mission_ack_decode(&msg, &value);
    
    json j;
    to_json(value, j);
    
    return j.dump();
}

std::string Decode(const MavLink_Pack_t& pack)
{
    mavlink_message_t msg;
    mavlink_status_t status;
    std::uint8_t chan=MAVLINK_COMM_0;
    std::string ans;
    for(int i=0;i<pack->buflen_;i++){
        if(mavlink_parse_char(chan, pack->buffer_[i],&msg, &status)==1){
            switch(msg.msgid){
                case MAVLINK_MSG_ID::MISSION_ACK:
                    ans=DecodeMissionAck(msg);
                    break;
                case MAVLINK_MSG_ID::MISSION_REQUEST:
                    ans=DecodeMissionRequest(msg);
                    break;
                case MAVLINK_MSG_ID::MISSION_REQUEST_INT:
                    ans = DecodeMissionRequestInt(msg);
                    break;
                case MAVLINK_MSG_ID::VFR_HUD:
                    ans=DecodeVfrHud(msg);
                    break;
                case MAVLINK_MSG_ID::BATTERY_STATUS:
                    ans=DecodeBatteryStatus(msg);
                    break;
                case MAVLINK_MSG_ID::GPS_RAW_INT:
                    ans=DecodeGpsRawInt(msg);
                    break;
                case MAVLINK_MSG_ID::ATTITUDE:
                    ans=DecodeAttitude(msg);
                    break;
                case MAVLINK_MSG_ID::PARAM_REQUEST_LIST:
                    ans=DecodeParamRequestList(msg);
                    break;
                case MAVLINK_MSG_ID::HEARTBEAT:
                    ans=DecodeHeartbeat(msg);
                    break;
                default:
                    std::uint32_t cmd=msg.msgid;
                    json j;j["mav_cmd"]=cmd;
                    ans=j.dump();
                    break;
            }
        }
    }
    return ans;
}