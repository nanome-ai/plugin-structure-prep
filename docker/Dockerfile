FROM nanome/plugin-env

ENV ARGS=''

ARG CACHEBUST
RUN git clone https://github.com/nanome-ai/nanome-lib.git && cd nanome-lib && \
  git checkout nanobabel_fallback && pip install .

COPY . /app
WORKDIR /app

CMD python3 run.py ${ARGS}
