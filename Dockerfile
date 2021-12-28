FROM python:3.9.1-alpine
RUN pip install pipenv

RUN apk add postgresql postgresql-contrib postgresql-dev g++ curl linux-headers
COPY Pipfile .
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD tail -f terraform.tfstate
