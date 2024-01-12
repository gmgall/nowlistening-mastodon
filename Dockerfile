FROM python:slim
RUN pip3 install --no-cache-dir --upgrade pylast mastodon.py

WORKDIR /usr/app/mastofm
COPY update.py ./
COPY LICENSE ./
CMD [ "/bin/sh", "-c", "echo 'Iniciando os trabalhos...'; python3 ./update.py; echo 'Dormindo por dois minutos...'; while true; do sleep 120; python3 ./update.py; echo 'Dormindo por dois minutos...'; done" ]