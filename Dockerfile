FROM python:3.9

ARG discordToken

WORKDIR /Wynncord

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENV TOKEN=$discordToken

COPY . .

CMD ["python", "main.py"]