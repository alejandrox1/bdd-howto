FROM python:3.7.4-stretch

WORKDIR /src/app

RUN useradd -u 1000 -ms /bin/bash -G sudo user \
    && echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN apt-get update -y \
    && apt-get install -y vim bash-completion \
    && pip install pytest yapf \
    && pip install behave
