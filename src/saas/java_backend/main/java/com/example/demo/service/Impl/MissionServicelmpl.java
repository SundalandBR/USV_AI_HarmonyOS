
package com.example.demo.service.Impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;


import com.example.demo.mapper.MissionMapper;
import com.example.demo.pojo.Mission;
import com.example.demo.service.IMissionService;
import org.springframework.stereotype.Service;

@Service
public class MissionServicelmpl extends ServiceImpl<MissionMapper, Mission> implements IMissionService {


}
