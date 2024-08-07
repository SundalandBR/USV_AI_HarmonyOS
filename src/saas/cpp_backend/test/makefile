.PHONY:all
all:httptest datatest jsoncpptest sqltest

httptest:HttpTest.cpp ../Http/httplib.cc ../JsonCpp/json.hpp
	g++ -o $@  $^ -lpthread

datatest:DataTest.cpp ../JsonCpp/json.hpp ../Data/Data.hpp ../MysqlCpp/mysql.hpp
	g++ -o $@ $^ -lmysqlclient

jsoncpptest:JsonCppTest.cpp ../JsonCpp/json.hpp
	g++ -o $@ $^
	
sqltest:SqlTest.cpp ../Data/Data.hpp
	g++ -o $@ $^
.PHONY:clean
clean:
	rm -f httptest datatest jsoncpptest sqltest