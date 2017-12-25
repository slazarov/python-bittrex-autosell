# Use an official Python runtime as a parent image
FROM python:3.6.3-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app


# Install any needed packages specified in requirements.txt
RUN   apk update && apk add --no-cache --virtual git  && \
      pip install git+https://github.com/slazarov/python-bittrex-autosell.git && \
      rm -rf /var/cache/apk/*

ENTRYPOINT ["pba"]

CMD ["--coins","ZEN,BTC,SALT",\
    "--price","0.02",\
    "--time","5400",\
    "--log"]
