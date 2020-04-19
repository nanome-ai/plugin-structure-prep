FROM nanome/nanobabel
ENV ARGS=""

RUN apt install software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt update --fix-missing
RUN apt install -y python3.7 python3-pip git

ARG CACHEBUST
RUN git clone https://github.com/nanome-ai/nanome.git -b nanobabel_fallback
RUN cd nanome && python3.7 -m pip install .

# RUN python3.7 -m pip install nanome

COPY . /app
WORKDIR /app

CMD python3.7 run.py ${ARGS}
