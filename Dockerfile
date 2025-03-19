# Prepare the base environment.
FROM ubuntu:24.04 AS builder_base_spatial_layer_monitor

LABEL maintainer="asi@dbca.wa.gov.au"
LABEL org.opencontainers.image.source="https://github.com/dbca-wa/spatial-layer-monitor"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Australia/Perth
ENV PRODUCTION_EMAIL=True
ENV SECRET_KEY="ThisisNotRealKey"
SHELL ["/bin/bash", "-c"]
# Use Australian Mirrors
RUN sed 's/archive.ubuntu.com/au.archive.ubuntu.com/g' /etc/apt/sources.list > /etc/apt/sourcesau.list
RUN mv /etc/apt/sourcesau.list /etc/apt/sources.list
# Use Australian Mirrors

# Key for Build purposes only
ENV FIELD_ENCRYPTION_KEY="Mv12YKHFm4WgTXMqvnoUUMZPpxx1ZnlFkfGzwactcdM="

# Key for Build purposes only
RUN apt-get clean && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    binutils \
    build-essential \
    cron \
    gcc \
    git \
    htop \
    iputils-ping \
    libgdal-dev \
    libmagic-dev \
    libpq-dev \
    libproj-dev \
    libreoffice \
    mtr  \
    p7zip-full \
    patch \
    postgresql-client \
    postgresql-client \
    python3 \
    python3-azure \
    python3-dev \
    python3-gunicorn \
    python3-pip \
    python3-setuptools \
    software-properties-common \
    sqlite3 \
    ssh \
    tzdata \
    vim \
    virtualenv \
    wget

# Install newer gdal version that is secure
RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    gdal-bin \
    python3-gdal

RUN ln -s /usr/bin/python3 /usr/bin/python 

RUN groupadd -g 5000 oim 
RUN useradd -g 5000 -u 5000 oim -s /bin/bash -d /app
RUN mkdir /app 
RUN chown -R oim.oim /app 

# Default Scripts
RUN wget https://raw.githubusercontent.com/dbca-wa/wagov_utils/main/wagov_utils/bin/default_script_installer.sh -O /tmp/default_script_installer.sh
RUN chmod 755 /tmp/default_script_installer.sh
RUN /tmp/default_script_installer.sh

RUN apt-get install --no-install-recommends -y python3-pil

ENV TZ=Australia/Perth
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY startup.sh /
RUN chmod 755 /startup.sh

# Install Python libs from requirements.txt.
FROM builder_base_spatial_layer_monitor AS python_libs_spatial_layer_monitor
WORKDIR /app
USER oim 
RUN virtualenv /app/venv
ENV PATH=/app/venv/bin:$PATH
RUN git config --global --add safe.directory /app

COPY requirements.txt ./
COPY python-cron ./
RUN whoami
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt 

COPY --chown=oim:oim spatial_layer_monitor spatial_layer_monitor
#COPY --chown=oim:oim thermalimageprocessing thermalimageprocessing
COPY --chown=oim:oim manage.py ./
RUN python manage.py collectstatic --noinput

# Install the project (ensure that frontend projects have been built prior to this step).
FROM python_libs_spatial_layer_monitor
COPY timezone /etc/timezone
COPY gunicorn.ini ./

COPY .git ./.git

EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/startup.sh"]
