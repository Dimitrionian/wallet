# Use an official Python runtime as a parent image
FROM python:3.11

# Install core libs
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  apt-utils \
  netcat-traditional \
  binutils \
  libproj-dev \
  libpq-dev \
  gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry poetry-plugin-export

# Limited scope (User) context
# Prepare app user
RUN useradd --create-home app

# Set the working directory
WORKDIR /home/app

# Install source code
RUN mkdir -p /home/app/libs
WORKDIR /home/app/libs
ENV PYTHONPATH="/home/app/libs"

# Init static
RUN mkdir -p /var/www/static && chown -R app:app /var/www/static
RUN chmod +664 -R /home/app

# Init media
RUN mkdir -p /var/www/media && chown -R app:app /var/www/media
VOLUME ["/var/www/media"]

USER app
EXPOSE 8000

FROM python-base

ARG DOCKER_BUILD_REQUIREMENTS=requirements.txt
ENV DOCKER_BUILD_ENVIRONMENT=${DOCKER_BUILD_ENVIRONMENT}
ENV DJANGO_SETTINGS_MODULE=wallet.settings
ENV ROOT_PATH_FOR_DYNACONF=/home/app/config

USER root

# Install deps
COPY $DOCKER_BUILD_REQUIREMENTS /tmp/install/
WORKDIR /tmp/install
RUN pip install -r $DOCKER_BUILD_REQUIREMENTS

# Prepare Gunicorn Conf
#RUN id app >/dev/null 2>&1 || useradd -m app
#COPY --chown=app ./config /home/app/config/

# Move app source
COPY --chown=app ./src /home/app/libs/

RUN chmod +664 -R /home/app
RUN chmod +x -R /home/app/libs

WORKDIR /home/app/libs

USER app
# NOTE: Do not set ENTRYPOINT as this image will become incompatible with PyCharm Remote Debugger
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
