FROM brsynth/rpcache:dev

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY rpToolCache.py /home/
COPY tool_rpExtractSink.py /home/

RUN python rpToolCache.py
