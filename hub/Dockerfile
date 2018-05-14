ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub-onbuild:$JUPYTERHUB_VERSION

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get install -y libpq-dev \
    && apt-get autoremove -y \
    && apt-get clean -y

RUN pip install --upgrade pip

RUN pip3 install psycopg2 \
    && pip3 install oauthenticator \
    && pip3 install dockerspawner \
    && pip3 install oauthenticator \
    && pip3 install jupyterlab

RUN groupadd jsp
RUN useradd -m -g jsp -p $(openssl passwd -1 jsp) jsp
RUN chown jsp:jsp .

RUN mkdir -p /srv/jupyterhub/ssl
RUN chmod 700 /srv/jupyterhub/ssl

COPY secrets/ssl* /srv/jupyterhub/ssl/
COPY jupyterhub_config.py /srv/jupyterhub/
RUN ls -la /srv/jupyterhub/ssl/*
RUN chmod 600 /srv/jupyterhub/ssl/*

RUN chown -R jsp:jsp /srv/jupyterhub

#USER jsp
