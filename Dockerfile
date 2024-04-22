# use the official Python image from the Docker Hub
FROM python:3.10-slim

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY ./requirements.txt /code/requirements.txt

# inatall dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy the content of the local src directory to the working directory
COPY ./website /code/app

# set the working directory in the container
WORKDIR /code/app

# install imagemagick
RUN apt install imagemagick

# run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

# expose the port 5000
EXPOSE 5000