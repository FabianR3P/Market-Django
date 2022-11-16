# base image
FROM python:3

#maintainer
LABEL Author="CodeGenes"

#directory to store app source code
RUN mkdir /market

#switch to /app directory so that everything runs from here
WORKDIR /market

#copy the app code to image working directory
COPY ./market /market

#let pip install required packages
RUN pip install -r requirements.txt