FROM brsynth/rpcache:dev

RUN pip install --no-cache-dir cobra

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY galaxy/code/tool_rpExtractSink.py /home/
