
package com.example.demo.service.Impl;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.demo.mapper.UserMapper;
import com.example.demo.pojo.User;
import com.example.demo.service.IUserService;
import org.springframework.stereotype.Service;

@Service
public class UserServicelmpl extends ServiceImpl<UserMapper, User> implements IUserService {



}
