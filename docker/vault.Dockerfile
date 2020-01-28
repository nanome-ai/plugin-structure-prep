FROM python:3.7

COPY . /app
WORKDIR /app
RUN pip install nanome
RUN ln -s ./nanobabel/nanobabel.exe /bin/usr/local/

CMD ["python", "-m", "nanome_structure_prep.StructurePrep", "-a", "localhost"]