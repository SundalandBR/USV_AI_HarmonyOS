package com.example.demo.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

@TableName("video_data")
public class Video {
    @TableId(value = "video_id",type = IdType.AUTO)
    public int videoId;
    public String filePath;
    public int fileSize;
    public float  duration;
    public float resolution;
}
