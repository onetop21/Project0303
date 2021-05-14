# Stage 1
FROM    ubuntu:18.04

RUN     apt update
RUN     apt upgrade -y
RUN     apt install git curl zip -y

WORKDIR /build
RUN     git clone https://github.com/flutter/flutter.git -b stable
ENV     PATH="/build/flutter/bin:${PATH}"
RUN     flutter precache

COPY    frontend frontend
WORKDIR /build/frontend
RUN     flutter pub get
RUN     flutter build web --release

# Stage 2
FROM    python:3.8

COPY    requirements.txt requirements.txt
RUN     pip install -r requirements.txt

WORKDIR /release
COPY    --from=0 /build/frontend/build/web /release/frontend/build/web
COPY    service service

CMD     python service
