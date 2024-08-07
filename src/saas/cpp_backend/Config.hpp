#ifndef __CONFIG_HPP
#define __CONFIG_HPP

#include <map>
#include <memory>
#include <iostream>
#include <fstream>

namespace config
{   
    /**
     * @brief 可以接受/返回任意类型的参数
     * @attention 类型转换失败会抛出异常
     * 
     * Example: usage:
     * ```
     *  Any a_int(5);
     *  int i=a_int.cast<int>();
     * ```
     */
    class Any
    {
    public:
        Any()=default;
        ~Any()=default;
        Any(const Any& any)=delete;
        Any& operator=(const Any& any)=delete;
        Any(Any&& any)=default;
        Any& operator=(Any&& any)=default;

        template <typename T>
        Any(T data):base_(new Derive<T>(data)){}

        template <typename T>
        T cast()
        {
            Derive<T>* derive=dynamic_cast<Derive<T>*>(base_.get());
            if(nullptr==derive) throw std::string(__FILE__)+" in "+std::string(__LINE__)+": "+"Conversion failure";
            return derive->data_;
        }

    private:
        class Base
        {
        public:
            virtual ~Base()=default;
        };
        template <typename T>
        class Derive:public Base
        {
        public:
            Derive(T data): data_(data){}

            T data_;
        };
        
        std::unique_ptr<Base> base_;
    };

    /**
     * @brief 解析类
     */
    class Config
    {   
    public:
        Config()=default;

        Config(const std::string& path)
        {
            load(path);
        }

        std::string get(const std::string& k)
        {
            auto it=kvs.find(k);
            if(it==kvs.end()) return nullptr;
            return it->second;
        }

        void load(const std::string& path)
        {
            std::ifstream in(path);
            if(!in.is_open()){
                std::cerr<<"file open fail"<<std::endl;
                exit(-1);
            }

            std::string line;
            kvs.clear();
            while(getline(in,line)){
                if(line.empty()||line[0]=='#') continue;
                auto vst=line.find("=");
                auto ven=line.find("\n");
                kvs[line.substr(0,vst)]=line.substr(vst+1,ven-vst-1);
            }

            in.close();
        }
    private:
        std::map<std::string,std::string> kvs;
    };
}

#endif