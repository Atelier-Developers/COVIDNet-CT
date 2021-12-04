FROM alpharmike/covid-net-ct:latest

RUN pip3 install pydicom && \
    pip3 install Pillow

RUN git pull

CMD ["tail", "-f", "/dev/null"]
