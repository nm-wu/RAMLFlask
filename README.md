# FlaskRAML
FlaskRAML is a tool that allows the development of web APIs with Flask, in combination with Domain-Specific Language (DSL) inputs based on RAML. This is a proof of concept implementation, accompanied by a thesis on the topic. One goal of this tool was providing Roundtrip Engineering support for this DSL integration. This means that DSL code and handwritten extensions of it can be evolved separately, and then integrated again over time. This should improve the development experience of Flask with RAML.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. First off, you will need a copy of this repository. Then, you can just reference the FlaskRAML files in your project to utilise them. Second, you will need to make sure that you have all the dependencies installed. To do this, you can use the requirements.txt file. This file contains all necessary requirements for the project. You can use pip to install all the requirements in that file
``` python
pip install -r requirements.txt
```
Please note that the project was done using Python 2.7.10 Thus, you should also use a version of Python 2 to run this project.

## Creating a simple application
Creating a basic application essentially involves creating a RAML file, and then referencing it via RAMLFlask. To only run the generated code, this minimal example will work, independent of the contents of the RAML file. Additional code is only needed to include handwritten code extensions.

For this, you first have to include the necessary dependencies to the following RAMLFlask classes: Generator, Comparison, and Server. The Generator class is responsible for generating the code artifacts. Then, the Comparison class allows for checks against previous versions of the RAML file, to notify the developer of any changes that would require their attention. Finally, the Server class is actually used for creating a Flask server based on the previous two components.
``` python
from RAMLFlask.Generator import Generator
from RAMLFlask.Comparison import Comparison
from RAMLFlask.Server import Server
```
The creation of a simple server then utilizes these dependencies and references a RAML file.
``` python
gen = Generator('./example.raml')
comp = Comparison()
Server(gen, comp).exec_all()
```

If you want to start the regular execution of the project with the provided files, you can execute
``` python
python main.py
```
Please be aware that the URL of the route might also contain the version of the API, if present in the RAML file. The version would be found before the rest of the URL. As an example: URL/**v1**/resource. Of course, you could also change the code in this example and use it for your own project.

## Running the tests
This repository contains several tests, which should help verify that FlaskRAML is implemented correctly, and actually delivers the benefits mentioned before. Below, each test is described. These tests allow to replicate all evaluation measurements mentioned in the corresponding thesis document.

### Unit tests
FlaskRAML includes a collection of unit tests, with the purpose of verifying that all functions created for FlaskRAML are working as intended. This should help confirm that the current version of FlaskRAML is working, which also makes it suitable for continued development while verifying that everything is working as intended. The unit tests can be started via
``` python
python RAMLFlask_tests/main.py
```

### Evolution test
Different versions of the same API will have to undergo changes to both handwritten as well as generated code. Changes in the generated code might also affect the handwritten code, for example if a variable is removed. This test confirms the ability of FlaskRAML to provide notifications to the developers, to signal if changes in the generated code could affect hanndwritten code. Recreating the evolution tests is a bit more involved: it includes running
``` python
python evolution_test.py
```
For each new version of the evolution, the file has to be changed to reflect the current version, before execution.

### Memory test
This test can be used to run several RAML specifications of real-world APIs, to then test the memory utilization for each of the APIs in each stage of the FlaskRAML execution process. This should help to ensure that FlaskRAML is not using too much memory, so that it can actually be run on most machines. The memory test can be started via
``` python
python mem_tester.py
```
This test uses mprof, thus the path for mprof should be set correctly for this test to work.
```
PATH=/path/to/mprof:$PATH python mem_tester.py
```

### Performance test
This test can be used to run several RAML specifications of real-world APIs, to then test the build performance for each of the APIs in each stage of the FlaskRAML execution process. This should help to ensure that FlaskRAML is performing well enough for real-world usage. The performance test can be started via
``` python
python performance_test.py
```

## License
This project is licensed under the BSD-3 License - see the LICENSE.md file for details
