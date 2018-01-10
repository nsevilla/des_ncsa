# Dockerfile for des_ncsa
# Matias Carrasco Kind <mgckind@gmail.com>
FROM python:3
WORKDIR /des
# Basic python reqs
RUN pip install --no-cache-dir tornado
RUN pip install --no-cache-dir jira
RUN pip install --no-cache-dir netaddr
RUN pip install --no-cache-dir bcrypt
# Copy code
ADD des_public_new/ /des/
ADD .access /des/.access
CMD [ "python", "main.py" ]

