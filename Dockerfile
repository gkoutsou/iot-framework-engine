FROM erlang:18

# MAINTAINER Konstantinos Vandikas (konstantinos.vandikas@ericsson.com)

# install git and checkout source-code from github
RUN apt-get update
RUN apt-get install -yq git curl wget # software-properties-common 
WORKDIR /opt/iot-framework-engine
# RUN git clone https://github.com/EricssonResearch/iot-framework-engine.git

# configure repositories
# RUN add-apt-repository ppa:chris-lea/node.js
# RUN add-apt-repository "deb http://ftp.sunet.se/pub/lang/CRAN/bin/linux/ubuntu trusty/"
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs

# update/upgrade base system
RUN apt-get update
RUN apt-get -yq upgrade

# install misc dependencies
RUN apt-get install -yq xsltproc python-pip libpython-dev

# install erlang
# RUN apt-get install -yq erlang

# install nodejs
RUN apt-get install -yq python g++ make
# RUN apt-get install -yq nodejs

# install R
RUN apt-get install -yq r-base --force-yes
RUN apt-get install -yq openjdk-8-jre vim

COPY . .

# install semantic-adapter
# WORKDIR /opt/iot-framework-engine
# RUN pip install -r semantic-adapter/pip-freeze.txt

# compilation
# WORKDIR /opt/iot-framework-engine
RUN which rebar
RUN which rebar3
RUN find / | grep erl_interface

RUN mkdir -p /usr/lib/erlang/lib/ && ln -s /usr/local/lib/erlang/lib/erl_interface-3.8.2/ /usr/lib/erlang/lib/erl_interface-3.7.13 # hack..
RUN make install

# expose port
EXPOSE 8000
EXPOSE 9200
EXPOSE 9300

# Start the IoT-Framework
CMD ./scripts/sensec_light.sh start