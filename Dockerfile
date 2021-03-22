# Node container does the npm stuff
FROM node AS build-stage

# Copy stuff from React to root
WORKDIR /react
COPY react/. .

# Must be set as the public URL
ENV REACT_APP_BASE_URL=https://bbotlhouse-surprise-me.herokuapp.com/

# React install and build
RUN npm install
RUN npm run build

# Python container runs the app
FROM python:3.9

# Production environment variables go here
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV SQLALCHEMY_ECHO=True

# Punch a hole at 8000
EXPOSE 8000

# Copy app to workdir
WORKDIR /usr/src/app
COPY . .
COPY --from=build-stage /react/build/* app/static/

# Install dependencies
RUN pip install -r requirements.txt
RUN pip install psycopg2

# Run the app
CMD gunicorn --worker-class eventlet -w 1 app:app
