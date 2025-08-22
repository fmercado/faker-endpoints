# Use the official Python runtime image
FROM python:3.13

# Create the app directory
RUN mkdir /var/app

# Set the working directory inside the container
WORKDIR /var/app

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

COPY poetry.lock pyproject.toml /var/app
RUN pip3 cache purge
RUN pip3 install -U pip setuptools
RUN pip3 install poetry==2.1.3
RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install
RUN pip install typing_extensions


# Copy the Django project to the container
COPY endpointer /var/app/

RUN rm -f db.sqlite3

# Expose the Django port
EXPOSE 8100

# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8100"]