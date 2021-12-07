FROM alpharmike/covid-net-ct:latest

RUN apt-get update && \
  apt-get install -y build-essential qt5-default \
  --no-install-recommends

RUN pip3 install pydicom && \
    pip3 install Pillow && \
    pip3 install prometheus-client


WORKDIR interface

RUN qmake interface.pro && make

WORKDIR /app/COVIDNet-CT

CMD ["python", "main.py"]
