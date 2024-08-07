package com.example.demo.pojo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import org.apache.ibatis.type.NStringTypeHandler;

@TableName("user_accounts")
public class User {
    @TableId(value = "user_id",type = IdType.AUTO)
    public int userId;
    public String username;
    public String password;
    public String phoneNumber;
    public String devUuidList;
    public String missionIdList;
}
