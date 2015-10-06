# IoT-Framework Engine

The IoT-Framework is a computational engine for the Internet of Things (IoT). It was developed jointly by Ericsson Research, the Swedish Institute of Computer Science (SICS) and Uppsala University in the scope of Project CS 2013. This repository contains the server side of the system, while [IoT-Framework-GUI](https://github.com/EricssonResearch/iot-framework-gui) contains the graphical user interface.

## Demo

You can check out a demo of the IoT-Framework here: [IoT-Framework demo](https://vimeo.com/98966770).

## Installing the project

1. Download and compile the linux system dependencies, (only needed once per machine)

        make install_linux_deps

2. Download and compile the project dependencies, and compile the project sources

        make install

## Running the project

1. Run the application by using startup script (one of the commands below)

        make run_all
  
  or
  
        sudo ./scripts/sensec.sh start

2. Alternative run (type each in separate shells)

        make run_rabbit
        make run_es
        make run_nodejs
        % don't forget to export R_HOME for example
        export R_HOME="/usr/lib/R"
        make run

4. To shutdown either close each individual shell or run one of the commands below

        make stop_all

   or
   
        sudo ./scripts/sensec.sh stop

## Running the project via Docker

1. Retrieve the Dockerfile
2. Build the docker image
        
        docker build -t username/image_name:version home_directory
        (or more concretely) docker build -t costa@iot-f:v1 .

3. Run the image
        
        docker run -p 8080 -dti username/image_name:version 
        (or more concretely) docker run -p -dti costa@iot-f:v1

4. Check if the system is running. This command should show if the system is running properly and also the port mapping that has been made for port 8080.

        docker ps
        

## Running tests

1. There are two ways of setting up the environment for testing. Either run the startup script by one of the below commands.

        make test_setup
        sudo ./scripts/sensec.sh test_setup

2. Or run each of the following commands in a separate shell

        make run_rabbit
        make run_es
        make run_nodejs
        make run_fake_resource

3. Run the tests

        make test

## Code Status

[![Build Status](https://travis-ci.org/EricssonResearch/iot-framework-engine.svg)](https://travis-ci.org/EricssonResearch/iot-framework-engine)
