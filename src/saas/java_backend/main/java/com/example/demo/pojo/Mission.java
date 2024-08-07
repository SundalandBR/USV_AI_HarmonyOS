package com.example.demo.pojo;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

@TableName("mission_data")
public class Mission{
    @TableId(value = "mission_id",type = IdType.AUTO)
    public Integer missionId;
    public Integer userId;
    public String createTime;
    public String finishTime;
    public String positionList;
    public Integer status;
    public Integer priority;//优先级
    public String waterDataIdList;
    public String navigationIdList;
    public String description;
    public int videoId;
}
