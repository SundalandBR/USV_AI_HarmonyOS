package com.example.demo.vo;

public class Result <T>{
    public int code;
    public String msg;
    public T Data;

    public static <T>Result Success(){
        Result r = new Result();
        r.code=1;
        r.msg="suc";
        return r;
    }
    public static <T>Result Success(T Data){
        Result r = Success();
        r.Data=Data;
        return r;
    }
    public static Result fail(String Text){
        Result r = new Result();
        r.code=0;
        r.msg=Text;
        return r;
    }


}
