# 
FROM python:3.10-slim

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./website /code/app

#
WORKDIR /code/app

#
RUN pip install 

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

#
EXPOSE 5000