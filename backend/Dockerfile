# Set base image
ARG BASE_IMAGE=ubuntu:22.04
FROM $BASE_IMAGE

# Install GPU-enabled version of PyTorch if set
ARG GPU

# Target CPU architecture
ARG TARGETARCH

# Set Python version (i.e. 3, 3.8)
ARG PYTHON_VERSION=3.10
# List of txtai components to install
ARG COMPONENTS=[]

# Locale environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set default working directory
WORKDIR /usr/src/

COPY ./requirements.txt requirements.txt
COPY ./entrypoint-backend.sh ./entrypoint-backend.sh
RUN ["chmod", "+x", "./entrypoint-backend.sh"]

RUN \
    # Install required packages
    apt-get update && \
    apt-get -y --no-install-recommends install curl libpq-dev libgomp1 libsndfile1 gcc g++ python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python3-pip && \
    rm -rf /var/lib/apt/lists && \
    \
    # Install txtai project and dependencies
    ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python && \
    python -m pip install --no-cache-dir -U pip wheel setuptools && \
    python -m pip install --no-cache-dir --upgrade -r requirements.txt && \
    if [ -z ${GPU} ] && { [ -z ${TARGETARCH} ] || [ ${TARGETARCH} = "amd64" ] ;}; then pip install --no-cache-dir torch==2.3.0+cpu torchvision==0.18.0+cpu -f https://download.pytorch.org/whl/torch_stable.html; fi && \
    python -m pip install --no-cache-dir txtai${COMPONENTS} && \
    python -c "import sys, importlib.util as util; 1 if util.find_spec('nltk') else sys.exit(); import nltk; nltk.download('punkt')" && \
    \
    # Cleanup build packages
    apt-get -y purge gcc g++ python${PYTHON_VERSION}-dev && apt-get -y autoremove

# Set default working directory
WORKDIR /usr/src/app
