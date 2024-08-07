

package com.example.demo.service.Impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;


import com.example.demo.mapper.NavigationMapper;
import com.example.demo.pojo.Navigation;
import com.example.demo.service.INavigationService;
import org.springframework.stereotype.Service;

@Service
public class NavigationServiceImpl extends ServiceImpl<NavigationMapper, Navigation> implements INavigationService {


}