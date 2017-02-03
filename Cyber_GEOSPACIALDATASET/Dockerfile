FROM python:2

WORKDIR /app

ENV GOSU_VERSION 1.7

RUN set -x \
    && apt-get update -yqq && apt-get install -yqq --no-install-recommends ca-certificates wget && rm -rf /var/lib/apt/lists/* \
    && wget -qO /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture)" \
    && wget -qO /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture).asc" \
    && export GNUPGHOME="$(mktemp -d)" \
    && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
    && gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu \
    && rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu \
    && gosu nobody true \
    && apt-get purge -y --auto-remove ca-certificates wget

RUN set -x \
    && apt-get update -qy \
    && apt-get install -y gawk s3cmd \
    && pip install requests \
    && groupadd -g 12001 cyberbot \
    && useradd -m -u 12001 -g 12001 -s /bin/bash cyberbot \
    && rm -rf /var/lib/apt/lists/*

ADD r.sh gio_1.py gio_3.py /app/

CMD ["/app/r.sh"]
