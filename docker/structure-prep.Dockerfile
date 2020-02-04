FROM python:3.7

COPY . /app
WORKDIR /app
RUN pip install ./nanome

CMD ["python", "-m", "nanome_structure_prep.StructurePrep", "-a", "localhost"]