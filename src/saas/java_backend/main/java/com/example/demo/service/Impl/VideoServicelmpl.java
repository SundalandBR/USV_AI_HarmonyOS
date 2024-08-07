
package com.example.demo.service.Impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;


import com.example.demo.mapper.VideoMapper;
import com.example.demo.pojo.Video;
import com.example.demo.service.IVideoService;
import org.springframework.stereotype.Service;

@Service
public class VideoServicelmpl extends ServiceImpl<VideoMapper, Video> implements IVideoService {


}
