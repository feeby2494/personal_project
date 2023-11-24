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
COPY .flaskenv /usr/src/app/
COPY pyproject.toml /usr/src/app/
COPY setup.py /usr/src/app/ 
COPY wsgi.py /usr/src/app/
COPY api.egg-info/ /usr/src/app/api.egg-info
COPY api/ /usr/src/app/api

## Install requirements
RUN pip install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]