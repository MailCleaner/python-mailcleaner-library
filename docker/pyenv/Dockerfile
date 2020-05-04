FROM debian:jessie

ARG PYTHON_VERSION

WORKDIR /var/mailcleaner

ENV HOME="/var/mailcleaner"
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/bin:${HOME}/lib/openssl/bin:${PATH}"
ENV LD_LIBRARY_PATH="${HOME}/lib/openssl/lib"
ENV LDFLAGS="-L${HOME}/lib/openssl/lib -Wl,-rpath,${HOME}/lib/openssl/lib"
ENV CFLAGS="-I$HOME/lib/openssl/include"
ENV SSH="$HOME/lib/openssl"

RUN apt-get update && apt-get install -y aria2 git wget curl xz-utils \
  make build-essential llvm libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev libncurses5-dev libncursesw5-dev tk-dev libffi-dev liblzma-dev \
  && apt-get clean

RUN useradd mailcleaner -m -s /bin/bash -d /var/mailcleaner

RUN aria2c -q --checksum=sha-256=ddb04774f1e32f0c49751e21b67216ac87852ceb056b75209af2443400636d46 \
  https://www.openssl.org/source/openssl-1.1.1g.tar.gz
RUN tar xf openssl-1.1.1g.tar.gz

RUN cd openssl-1.1.1g \
  && ./config --prefix=$HOME/lib/openssl --openssldir=$HOME/lib/openssl no-ssl2 \
  && make \
  && make install \
  && cd ${HOME} \
  && rm -rf openssl-1.1.1g openssl-1.1.1g.tar.gz

RUN git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv \
  && pyenv install ${PYTHON_VERSION} \
  && pyenv local ${PYTHON_VERSION} \
  && pyenv exec pip install --upgrade pip

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
