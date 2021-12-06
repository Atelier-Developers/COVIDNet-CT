FROM alpharmike/covid-net-ct:latest

RUN pip3 install pydicom && \
    pip3 install Pillow

RUN git pull

WORKDIR interface

RUN qmake interface.pro && make

WORKDIR /app/COVIDNet-CT

CMD ["tail", "-f", "/dev/null"]
