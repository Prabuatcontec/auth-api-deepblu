FROM ubuntu:20.04
MAINTAINER  Prabu "<mprabu@gocontec.com>"
ENV TZ=America/Los_Angeles

COPY requirements.txt .
ENV FLASK_APP=app.py
ENV FLASK_ENV=development



RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -y \
  && apt-get install -y wget
RUN apt-get install -y gnupg
RUN apt-get install libzbar0 -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get -y install libmysqlclient-dev
RUN apt-get -y install gcc
RUN apt install -y git
RUN apt install -y cmake
RUN pip3 install -r requirements.txt
COPY .env .env
COPY . /apps
WORKDIR /apps


# install agent
RUN pip install newrelic

# env vars that control reporting
ENV NEW_RELIC_APP_NAME="api.auth.deepblu.com"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=a3e4b57556ffd8da9ac92b3005ac0f1ad43e684f
ENV NEW_RELIC_LOG_LEVEL=info


RUN pip install python-dotenv
RUN pip3 install pyyaml
RUN pip3 install requests
RUN pip3 install Flask-Session
RUN pip3 install flask flask-jsonpify flask-sqlalchemy flask_restplus
RUN pip3 freeze
RUN pip3 install mysqlclient

EXPOSE 9000
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 \
    CMD curl -f http://localhost:9000/api/health || exit 1
ENTRYPOINT [ "newrelic-admin", "run-program"]

CMD ["python3", "run.py"]