FROM python:3.7

ENV PLUGIN_SERVER=plugins.nanome.ai

COPY . /app
WORKDIR /app

RUN pip3 install ./nanome
RUN ln -s ./nanobabel/nanobabel.exe /usr/local/bin

CMD /bin/bash
# CMD python -m nanome_structure_prep.StructurePrep -a ${PLUGIN_SERVER}