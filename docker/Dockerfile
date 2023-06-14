FROM nanome/plugin-env

ENV ARGS=''
WORKDIR /app

ARG CACHEBUST
COPY requirements.txt .
RUN pip install -r requirements.txt

# Make sure DSSP has executable permissions.
# In some kubernetes environments, executable permissions can't be set
# by the lib, and must be set at build-time
ARG DSSP_PATH_LINUX=/opt/conda/lib/python3.9/site-packages/nanome/_internal/process/external/dssp/dssp-linux
ARG DSSP_PATH_WIN=/opt/conda/lib/python3.9/site-packages/nanome/_internal/process/external/dssp/dssp-3.0.0-win32.exe
RUN chmod +x ${DSSP_PATH_LINUX} ${DSSP_PATH_WIN}

COPY . .

CMD python run.py ${ARGS}
