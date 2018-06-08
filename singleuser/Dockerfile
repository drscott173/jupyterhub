#
# Build a compatible Nvidia container that we can
# use when spawning new user notebooks
#
FROM ufoym/deepo:all-py36-jupyter
ARG JUPYTERHUB_VERSION=0.8.1

RUN pip3 install wheel google google-auth dockerspawner oauthenticator jupyterlab bokeh
RUN pip install wheel google google-auth dockerspawner oauthenticator jupyterlab bokeh

# Install node and jupyterhub so we can
# run as containers on a local port
RUN apt-get -y update && \
    apt-get -y install nodejs npm nodejs-legacy && \
    npm install -g configurable-http-proxy

RUN pip3 install --no-cache \
    jupyterhub==$JUPYTERHUB_VERSION \
    'notebook>=5.0,<=6.0'

# install notebook modules for downloading
RUN apt-get -y install pandoc && \
    apt-get -y install texlive-xetex

# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]
CMD ["/usr/local/bin/jupyterhub-singleuser","--ip=0.0.0.0", "--allow-root"]

# Add startup files
WORKDIR /notebooks
RUN mkdir -p /notebooks
ADD https://raw.githubusercontent.com/aronchick/kubecon-demo/master/demo/notebooks/yelp.ipynb?token=AAG4Kr5E9cCjZ6FBBUQgf_04ulSUpIUQks5bIsrEwA%3D%3D \
    /notebooks/6_yelp_sentiment.ipynb
ADD https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/tools/docker/notebooks/1_hello_tensorflow.ipynb \
    /notebooks/1_hello_tensorflow.ipynb
ADD https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/tools/docker/notebooks/2_getting_started.ipynb \
    /notebooks/2_getting_started.ipynb
ADD https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/tools/docker/notebooks/3_mnist_from_scratch.ipynb \
    /notebooks/3_mnist_from_scratch.ipynb
ADD https://raw.githubusercontent.com/aymericdamien/TensorFlow-Examples/master/notebooks/6_MultiGPU/multigpu_basics.ipynb \
    /notebooks/4_multigpu_basics.ipynb
ADD https://raw.githubusercontent.com/aymericdamien/TensorFlow-Examples/master/notebooks/6_MultiGPU/multigpu_cnn.ipynb \
    /notebooks/5_multigpu_cnn.ipynb
ADD https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/tools/docker/notebooks/LICENSE \
    /notebooks/LICENSE
