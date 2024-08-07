package com.example.demo.pojo;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

@TableName("navigation_data")
public class Navigation {
    @TableId(value = "navigation_id",type = IdType.AUTO)
    public int navigationId;
    public int missionId;
    public String timestamp;
    public double latitude;
    public double longitude;
    public float speed;
    public float course;//角度
    public int status;
    public float batteryLevel;
}
