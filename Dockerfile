FROM brsynth/rpcache

COPY rpTool.py /home/
COPY rpToolServe.py /home/
#COPY rpToolCache.py /home/

#COPY test/inSBML.sbml.xml /home/
#COPY test/tool_rpExtractSink.py /home/

RUN rm -f /home/Dockerfile
