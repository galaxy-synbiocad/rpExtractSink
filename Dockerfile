FROM brsynth/rpbase:dev

RUN apt-get install --quiet --yes \
	libxext6  \
    	libxrender-dev  && \
    conda install -y -c rdkit rdkit && \
    mkdir input_cache && \
    wget https://www.metanetx.org/cgi-bin/mnxget/mnxref/chem_prop.tsv -P /home/input_cache/

COPY rpExtractSink.py /home/

#get rr_compounds.tsv
RUN wget https://retrorules.org/dl/this/is/not/a/secret/path/rr02 -O /home/rr02_more_data.tar.gz && \
    tar xf /home/rr02_more_data.tar.gz -C /home/ && \
    mv /home/rr02_more_data/compounds.tsv /home/input_cache/rr_compounds.tsv && \
    rm -r /home/rr02_more_data && \
    rm /home/rr02_more_data.tar.gz

RUN python rpExtractSink.py
