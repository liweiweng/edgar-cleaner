FROM python:3
LABEL version="1.0"
LABEL description="EDGAR CLEANER"
LABEL maintainer="mikaela.p.leal@ttu.edu"

RUN git clone https://github.com/mikaelapisani/edgar-cleaner.git

WORKDIR /root/edger-cleaner

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
VOLUME /root/data
VOLUME /root/masters
VOLUME /root/results

RUN sed -i 's/data_path=.*$/data_path=/root/data/' config.properties 
RUN sed -i 's/data_path=.*$/data_path=/root/masters' config.properties 
RUN sed -i 's/data_path=.*$/data_path=/root/results' config.properties 

