FROM nanome/plugin-env

ENV ARGS=''
WORKDIR /app

ARG CACHEBUST
COPY requirements.txt .
RUN pip install -r requirements.txt

# Make sure DSSP has executable permissions.
# In some environments, executable permissions can't be set
# by the lib, and must be set at build-time
ARG DSSP_PATH_LINUX=/opt/conda/lib/python3.9/site-packages/nanome/_internal/process/external/dssp/dssp-linux
RUN chmod +x ${DSSP_PATH_LINUX}

COPY . .

CMD python run.py ${ARGS}
