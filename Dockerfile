FROM python:3

WORKDIR /des_public

RUN pip install --no-cache-dir tornado
RUN pip install --no-cache-dir jira

COPY . .

CMD [ "python", "main.py" ]

