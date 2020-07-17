FROM brsynth/rpcache:v1

#RUN pip install --no-cache-dir cobra timeout-decorator
RUN pip install --no-cache-dir cobra==0.16 timeout-decorator

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY galaxy/code/tool_rpExtractSink.py /home/
