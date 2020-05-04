# Python 3.8.x and Jessie

An example for compiling Python 3.8.x with a Debian Jessie and pyenv.

## Usage

Build:

    $ docker build \
    --build-arg PYTHON_VERSION=$(cat ../../.python-version) \
    -t mailcleaner-pyenv .

Run:

    $ docker run -it --rm --name mailcleaner-pyenv \
    mailcleaner-pyenv python

Check Openssl version:
 
    $ docker run -it --rm --name mailcleaner-pyenv \
    mailcleaner-pyenv python -c "import ssl; print(ssl.OPENSSL_VERSION)"
