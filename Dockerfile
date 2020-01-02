FROM brsynth/rpcache

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY rpToolCache.py /home/
RUN rm -f /home/Dockerfile

#ENTRYPOINT ["python"]
#CMD ["/home/rpToolServe.py"]

# Open server port
#ONBUILD EXPOSE 8888
