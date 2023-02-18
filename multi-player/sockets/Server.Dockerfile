# use python runtime
FROM python:3-stretch

# set working dir
WORKDIR /docker_app

# copy socket server code into dir
COPY . /docker_app

RUN pip install pika  # normally it would be a requirements file, but in this case this is the only requirement, 
                      # therefore I decided to do it this way

# expose the ports i want to sue
EXPOSE 64001
EXPOSE 5672


# run
CMD ["python", "-u", "server.py"]