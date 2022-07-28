FROM python:3.9-slim
EXPOSE 8002
COPY . /code/
WORKDIR /code
RUN pip install -r requirement.txt
ENTRYPOINT ["sh", "entrypoint.sh"]