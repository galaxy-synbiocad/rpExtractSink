FROM brsynth/rpcache:dev

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY rpToolCache.py /home/
COPY galaxy_tool/tool_rpExtractSink.py /home/
