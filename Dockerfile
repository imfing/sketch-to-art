FROM node:10

# Configure packages needed
RUN apt-get update \
    # Install python3-pip
    && apt-get -y install python3-pip \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app

# Install Python dependencies
ADD server/requirements.txt /tmp/
RUN pip3 --no-cache-dir install -r /tmp/requirements.txt

# Install node packages
# ADD ./package.json ./yarn.* /tmp/
# RUN cd /tmp && yarn
# RUN cd /usr/src/app && ln -s /tmp/node_modules

# Download models
ADD server/models/download_models.sh /tmp/models/
RUN cd /tmp/models && sh ./download_models.sh

# Add project and change directory
ADD . /usr/src/app/
WORKDIR /usr/src/app

RUN cd server/models \
    && ln -s /tmp/models/wct \
    && ln -s /tmp/models/pix2pix

EXPOSE 8080 5001 5002
CMD ["bash", "run.sh"]
