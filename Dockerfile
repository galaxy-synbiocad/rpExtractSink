FROM brsynth/rpbase

RUN apt-get install --quiet --yes \
	libxext6  \
    	libxrender-dev  && \
    conda install -y -c rdkit rdkit && \
    mkdir input_cache && \
    wget https://www.metanetx.org/cgi-bin/mnxget/mnxref/chem_prop.tsv -P /home/input_cache/

COPY rpExtractSink.py /home/

RUN python rpExtractSink.py
