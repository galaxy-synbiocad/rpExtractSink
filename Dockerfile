FROM brsynth/rpcache

COPY rpTool.py /home/
COPY rpToolServe.py /home/

RUN rm -f /home/Dockerfile
