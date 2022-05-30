FROM python:3.7-slim-buster
WORKDIR /excel
COPY . /excel
RUN ls /excel
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python" ,"ex_to_graph.py"]
CMD ["a"]
