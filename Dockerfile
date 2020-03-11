FROM brsynth/rpcache:dev

RUN pip install --no-cache-dir cobra

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY rpToolCache.py /home/
COPY tool_rpExtractSink.py /home/

RUN python rpToolCache.py
