package com.example.demo.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

@TableName("water_quality_data")
public class WaterData {
    @TableId(value = "water_data_id",type = IdType.AUTO)
    public int waterDataId;
    public int missionId;
    public String timestamp;
    public double latitude;
    public double longitude;
    public float ph;
    public float dissolvedOxygen;
    public float conductivity;
    public float temperature;
    public float turbidity;
    public float ammoniaNitrogen;
    public float organicMatter;
}
