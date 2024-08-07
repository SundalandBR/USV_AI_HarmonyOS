package com.example.demo.service;

public interface ITokenService {

    String generateToken(String ip); // 根据id和设备uuid 生成一个新的令牌

   boolean verifyToken(String token,String ip); // 验证令牌的有效性

    void deleteToken(String token);

}
