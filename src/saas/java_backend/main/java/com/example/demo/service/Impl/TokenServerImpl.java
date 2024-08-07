package com.example.demo.service.Impl;

import com.example.demo.service.ITokenService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.UUID;
import java.util.concurrent.TimeUnit;

@Service
public class TokenServerImpl implements ITokenService {

    private static final Logger log = LoggerFactory.getLogger(TokenServerImpl.class);
    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @Override
    public String generateToken(String ip){
        String Token=UUID.randomUUID().toString();
        redisTemplate.opsForValue().set(Token,ip,30, TimeUnit.MINUTES);
        return Token;
    }


    @Override
    public boolean verifyToken(String token,String ip){
        boolean r=redisTemplate.hasKey(token);
        if(r){
            log.info("ip:{},token:{}",ip,token);
            String value = (String) redisTemplate.opsForValue().get(token);
            return value.equals(ip);
        }
        return false;
    }




    @Override
    public void deleteToken(String token){
        redisTemplate.delete(token);
    }

}
