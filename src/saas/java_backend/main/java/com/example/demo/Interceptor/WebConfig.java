package com.example.demo.Interceptor;


import com.example.demo.service.Impl.TokenServerImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;



@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Autowired
    private TokenServerImpl tokenService;
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new TokenInterceptor(tokenService)).addPathPatterns("/**").excludePathPatterns("poi/login_out", "/poi/login");
    }
}
