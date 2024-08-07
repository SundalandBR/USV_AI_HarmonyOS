package com.example.demo.Interceptor;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import com.example.demo.service.Impl.TokenServerImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;





@Component
public class TokenInterceptor implements HandlerInterceptor {

    private static final Logger log = LoggerFactory.getLogger(TokenInterceptor.class);

    TokenServerImpl tokenService;
    public TokenInterceptor(TokenServerImpl tokenService){
        this.tokenService =tokenService;
    }


    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("Authorization");
        log.info("token:{}", token);
        if(token == null || token.isEmpty()){
            return false;
        }
        String ip = request.getRemoteAddr();


        return tokenService.verifyToken(token, ip);
    }


}
