#FROM brsynth/rpcache-rest
FROM brsynth/rpcache

RUN conda install -c conda-forge flask-restful

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY rpToolCache.py /home/
COPY rpCache.py /home/
COPY rpSBML.py /home/

RUN python rpCache.py

RUN rm -f /home/Dockerfile

ENTRYPOINT ["python"]
CMD ["/home/rpToolServe.py"]

# Open server port
EXPOSE 8888
