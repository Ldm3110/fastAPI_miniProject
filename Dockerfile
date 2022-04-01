FROM python:3.8-alpine

WORKDIR /project

# copy just requirements.txt in the container
COPY requirements.txt .

RUN \
  pip install --upgrade pip &&\
  python -m pip install -r requirements.txt

# copy all the code in the container
COPY . .

# define port to execute the project
EXPOSE 80

CMD uvicorn app.main:app --host 0.0.0.0 --port 80