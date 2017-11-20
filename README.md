# FlaskRAML
FlaskRAML is a tool that allows the development of web APIs with Flask, in combination with Domain-Specific Language (DSL) inputs based on RAML. This is a proof of concept implementation, accompanied by a thesis on the topic. One goal of this tool was providing Roundtrip Engineering support for this DSL integration. This means that DSL code and handwritten extensions of it can be evolved separately, and then integrated again over time. This should improve the development experience of Flask with RAML.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. First off, you will need a copy of this repository. Then, you can just reference the FlaskRAML files in your project to utilise them.

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

## Running the tests
This repository contains several tests, which should help verify that FlaskRAML is implemented correctly, and actually delivers the benefits mentioned before. Below, each test is described. These tests allow to replicate all evaluation measurements mentioned in the corresponding thesis document.

### Unit tests
FlaskRAML incldues a collection of unit tests, with the purpose of verifying that all functions created for FlaskRAML are working as intended. This should help confirm that the current version of FlaskRAML is working, which also makes it suitable for continued development while verifying that everything is working as intended.

### Evolution test
Different versions of the same API will have to undergo changes to both handwritten as well as generated code. Changes in the generated code might also affect the handwritten code, for example if a variable is removed. This test confirms the ability of FlaskRAML to provide notifications to the developers, to signal if changes in the generated code could affect hanndwritten code.

### Memory test
This test can be used to run several RAML specifications of real-world APIs, to then test the memory utilization for each of the APIs in each stage of the FlaskRAML execution process. This should help to ensure that FlaskRAML is not using too much memory, so that it can actually be run on most machines.

### Performance test
This test can be used to run several RAML specifications of real-world APIs, to then test the build performance for each of the APIs in each stage of the FlaskRAML execution process. This should help to ensure that FlaskRAML is performing well enough for real-world usage.

## License
This project is licensed under the BSD-3 License - see the LICENSE.md file for details
