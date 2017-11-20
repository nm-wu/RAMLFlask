from RAMLFlask.Server import Server
from RAMLFlask.Generator import Generator
from RAMLFlask.Comparison import Comparison

comp = Comparison()

#Test 1
Server(Generator('./test1/v1.raml'), comp, 'test1/config1.ini').exec_all()
#Server(Generator('./test1/v2_3.raml'), comp, 'test1/config2_3.ini').exec_all()
#Server(Generator('./test1/v2_3.raml'), comp, 'test1/config2_3.ini').exec_all()
#Server(Generator('./test1/v4_5.raml'), comp, 'test1/config4.ini').exec_all()
#Server(Generator('./test1/v4_5.raml'), comp, 'test1/config5.ini').exec_all()

# Test 2
#Server(Generator('./test2/v1.raml'), comp, 'test2/config1.ini').exec_all()
#Server(Generator('./test2/v2_6.raml'), comp, 'test2/config2.ini').exec_all()
#Server(Generator('./test2/v2_6.raml'), comp, 'test2/config3.ini').exec_all()
#Server(Generator('./test2/v2_6.raml'), comp, 'test2/config4.ini').exec_all()
#Server(Generator('./test2/v2_6.raml'), comp, 'test2/config5.ini').exec_all()
#Server(Generator('./test2/v2_6.raml'), comp, 'test2/config6.ini').exec_all()

# Test 3
#Server(Generator('./test3/v1.raml'), comp, 'test3/config1.ini').exec_all()
#Server(Generator('./test3/v2_6.raml'), comp, 'test3/config2.ini').exec_all()
#Server(Generator('./test3/v2_6.raml'), comp, 'test3/config3.ini').exec_all()
#Server(Generator('./test3/v2_6.raml'), comp, 'test3/config4.ini').exec_all()
#Server(Generator('./test3/v2_6.raml'), comp, 'test3/config5.ini').exec_all()
#Server(Generator('./test3/v2_6.raml'), comp, 'test3/config6.ini').exec_all()