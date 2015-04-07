FROM debian:jessie

RUN apt-get update && \
    apt-get install -y python python-pip curl && \
    curl -sSL https://get.docker.com | sh && \
    apt-get clean -y

COPY . /tow_sources
RUN pip install -e /tow_sources
# RUN pip install tow


VOLUME ["/workspace"]
WORKDIR /workspace

ENTRYPOINT ["tow"]
