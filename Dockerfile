FROM brsynth/rpbase

RUN apt-get install --quiet --yes \
	libxext6  \
    	libxrender-dev  && \
    conda install -y -c rdkit rdkit

COPY rpExtractSink.py /home/

RUN python rpExtractSink.py
