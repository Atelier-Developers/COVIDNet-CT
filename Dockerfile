FROM alpharmike/covid-net-ct:latest

RUN apt-get update && \
  apt-get install -y build-essential qt5-default libqt5sql5-mysql \
  --no-install-recommends

RUN pip3 install pydicom && \
    pip3 install Pillow && \
    pip3 install prometheus-client && \
    pip3 install numpy && \
    pip3 install pylibjpeg pylibjpeg-libjpeg && \
    pip3 install pypng && \
    pip3 install SimpleITK && \
    pip3 install merry


WORKDIR interface

RUN qmake interface.pro && make

WORKDIR /app/COVIDNet-CT

ENV PROMETHEUS_MULTIPROC_DIR /app/COVIDNet-CT/multiprocess_metrics/

CMD ["python", "main.py"]
