FROM python:3
LABEL version="1.0"
LABEL description="EDGAR CLEANER"
LABEL maintainer="mikaela.p.leal@ttu.edu"

RUN git clone -b devel https://github.com/mikaelapisani/edgar-cleaner.git /root/edgar-cleaner

WORKDIR /root/edgar-cleaner

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
VOLUME /root/data
VOLUME /root/masters
VOLUME /root/results

RUN sed -i 's/data_path=.*$/data_path=\/root\/data\//' config.properties 
RUN sed -i 's/master_path=.*$/master_path=\/root\/masters/' config.properties 
RUN sed -i 's/results_path=.*$/results_path=\/root\/results/' config.properties 

