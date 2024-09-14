# Set base image
ARG BASE_IMAGE=ubuntu:22.04
FROM $BASE_IMAGE

# Install GPU-enabled version of PyTorch if set
ARG GPU

# Target CPU architecture
ARG TARGETARCH

# Set Python version (e.g., 3, 3.10)
ARG PYTHON_VERSION=3.10

# List of txtai components to install
ARG COMPONENTS=[]

# Locale environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set default working directory
WORKDIR /usr/src/

# Create a non-root user
# RUN useradd --create-home --shell /bin/bash appuser

# Copy necessary files
COPY ./config.json /opt/chatsql/config.json
COPY ./requirements.txt requirements.txt
COPY ./entrypoint-backend.sh ./entrypoint-backend.sh

# Make entrypoint script executable
RUN chmod +x ./entrypoint-backend.sh && \
    apt-get update && \
    apt-get -y --no-install-recommends install \
        curl \
        g++ \
        gcc \
        libgomp1 \
        libpq-dev \
        libsndfile1 \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-dev \
        python3-pip \
        tzdata && \
    rm -rf /var/lib/apt/lists/* && \
    \
    # Install Python packages and txtai components
    ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python && \
    python -m pip install --no-cache-dir -U pip wheel setuptools && \
    python -m pip install --no-cache-dir --upgrade -r requirements.txt && \
    if [ -z "${GPU}" ] && { [ -z "${TARGETARCH}" ] || [ "${TARGETARCH}" = "amd64" ]; }; then \
        pip install --no-cache-dir torch==2.3.0+cpu \
            torchvision==0.18.0+cpu \
            -f https://download.pytorch.org/whl/torch_stable.html; \
    fi && \
    python -m pip install --no-cache-dir txtai${COMPONENTS} && \
    python -c "import sys, importlib.util as util; 1 if util.find_spec('nltk') else sys.exit(); import nltk; nltk.download('punkt')" && \
    \
    # Cleanup build packages
    apt-get -y purge \
        g++ \
        gcc \
        python${PYTHON_VERSION}-dev && \
    apt-get -y autoremove

# Set default working directory
WORKDIR /usr/src/app

# Change ownership of the working directory to the non-root user
# RUN chown -R appuser:appuser /usr/src/app /opt/chatsql

# # Switch to the non-root user
# USER appuser
