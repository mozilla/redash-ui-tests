FROM ubuntu:xenial
LABEL maintainer "Raphael Pierzina <raphael@hackebrot.de>"

ENV DEBIAN_FRONTEND=noninteractive \
    MOZ_HEADLESS=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Set target versions for dependencies
ENV FIREFOX_VERSION=59.0 \
    GECKODRIVER_VERSION=0.20.0 \
    PIPENV_VERSION=11.7.2

# Install requirements to install tools
RUN dependencies=' \
        bzip2 \
        ca-certificates \
        curl \
        firefox \
		python3.6 \
        python-pip \
        python-setuptools \
        python-wheel \
    ' \
    && set -x \
    && apt-get -qq update && apt-get -qq install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get -qq update && apt-get -qq install --no-install-recommends -y $dependencies \
    && apt-get -y purge firefox \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Install Firefox and Geckodriver
RUN INSTALLER_DOWNLOAD_URL=https://raw.githubusercontent.com/hackebrot/install-firefox/master/install-firefox.sh \
    && curl $INSTALLER_DOWNLOAD_URL -sSf | sh -s -- --firefox $FIREFOX_VERSION --geckodriver $GECKODRIVER_VERSION

# Install pipenv
RUN pip install pipenv==$PIPENV_VERSION

# Create user with a home directory
ENV HOME /home/user
RUN useradd --create-home --home-dir $HOME user

# Copy all files to the container
COPY . $HOME/src/

# Change file permissions to user
RUN chown -R user:user $HOME

# Set working directory
WORKDIR $HOME/src

# Change from root to user
USER user

# Install dependencies under Python 3.6
RUN pipenv install --python=$(which python3.6)

ENTRYPOINT [ "pipenv", "run" ]

CMD ["pytest", "--driver", "Firefox", "--verify-base-url", "--variables", "variables.json", "--html", "report.html"]
