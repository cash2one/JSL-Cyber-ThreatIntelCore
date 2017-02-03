# Dockerfile for running combine
#
FROM ubuntu:14.04
RUN apt-get update && \
  apt-get dist-upgrade -y
RUN apt-get install -y --no-install-recommends \
  python-pip  \
  python-dev \
  build-essential \
  python-virtualenv \
  git && \

  groupadd -r combine && \
  useradd -r -g combine -d /home/combine -s /sbin/nologin -c "Combine user" combine

WORKDIR /home
RUN git clone https://github.com/JohnSnowLabs/JSL-Cyber-ThreatIntelCore.git && \
  chown -R combine:combine /home/combine && \
  cd combine && \
  pip install -r requirements.txt

USER combine
ENV HOME /home/combine
ENV USER combine
COPY combine.cfg /home/combine/
WORKDIR /home/combine
CMD ["python", "combine.py", "-e"]
