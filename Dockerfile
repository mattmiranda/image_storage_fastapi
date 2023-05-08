FROM python:3.9

# Create directory for the app
WORKDIR /code

# copy requirements file
COPY ./requirements.txt /code/requirements.txt

# install packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# move python app code
COPY ./app /code/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]