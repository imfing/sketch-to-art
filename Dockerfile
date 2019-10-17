FROM node:10

# Configure packages needed
RUN apt-get update \
    # Install python3-pip
    && apt-get -y install python3-pip \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app/
WORKDIR /usr/src/app

# Install pip dependencies
RUN pip3 --no-cache-dir install -r server/requirements.txt \
    && yarn

EXPOSE 8080 5001 5002
CMD ["./run.sh"]