from ubuntu:jammy

RUN apt-get update -qq && \
  apt-get install -qq -y

ENTRYPOINT ["tail", "-f", "/dev/null"]