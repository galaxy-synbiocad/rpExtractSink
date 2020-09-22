FROM brsynth/rpcache:v2

RUN rm -rf /usr/local/lib/python3.7/site-packages/ruamel*
RUN pip install --no-cache-dir cobra==0.16 timeout-decorator
#RUN pip install --no-cache-dir cobra

#RUN conda install -c bioconda cobra==0.16
#RUN pip install timeout-decorator

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY galaxy/code/tool_rpExtractSink.py /home/
