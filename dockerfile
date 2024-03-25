# Use an official Python runtime as a parent image
FROM python:3.8

ENV  HOME /root
# Set the working directory in the container
WORKDIR /usr/src/app
WORKDIR /root

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 8080


# # delay for the DB and the container upload
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Run app.py when the container launches
CMD /wait  && python -u ["flask", "run"],