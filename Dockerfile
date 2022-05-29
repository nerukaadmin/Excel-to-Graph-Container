FROM python:3.7-slim-buster
WORKDIR /excel
COPY ./IN /excel
COPY ./OUT /excel
COPY ./tmp /excel
COPY ex_to_graph.py /excel
COPY team_member_list.txt excel
COPY requirements.txt /excel
RUN ls /excel
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python" ,"ex_to_graph.py"]
CMD ["a"]
