# Image from https://hub.docker.com/ from images uploaded by nice devs
FROM python:3.10

# Display the python output through the terminal, these would go directly to docker log if not set
ENV PYTHONUNBUFFERED: 1

# Set work directory for our docker container, not our local OS!
WORKDIR /usr/src/app

# Add python dependencies
## Update pip
RUN pip install --upgrade pip

## Copy requirements
COPY requirements.txt ./requirements.txt

## Install requirements
RUN pip install -r requirements.txt

