FROM python:alpine
WORKDIR /usr/app/mastofm

RUN pip3 install pylast mastodon.py schedule python-dotenv --no-cache-dir --upgrade

COPY update.py .
COPY LICENSE .

RUN sed -i 's/ - / • /g' update.py
RUN sed -i 's/ 🔊//g' update.py

ENTRYPOINT [ "python3", "update.py" ]