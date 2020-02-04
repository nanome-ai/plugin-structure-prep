FROM continuumio/miniconda3 as conda

ENV PLUGIN_SERVER=localhost

COPY . /app
WORKDIR /app

RUN conda install -c openbabel openbabel
RUN pip install ./nanome

CMD python -m nanome_structure_prep.StructurePrep -a ${PLUGIN_SERVER}