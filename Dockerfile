FROM brsynth/rpcache

RUN pip install --no-cache-dir cobra==0.16

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY galaxy/code/tool_rpExtractSink.py /home/
