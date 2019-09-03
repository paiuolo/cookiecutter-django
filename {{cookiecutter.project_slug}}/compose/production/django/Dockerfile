{% if cookiecutter.js_task_runner == 'Gulp' -%}
FROM node:10-stretch-slim as client-builder

WORKDIR /app
COPY ./package.json /app
RUN npm install && npm cache clean --force
COPY . /app
RUN npm run build

# Python build stage
{%- endif %}
FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1


# pai
# config files
ENV APP_DOMAIN "{{ cookiecutter.domain_name }}"
ENV APP_DOMAINS "{{ cookiecutter.domain_name }}"


RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi


# pai
RUN apk add libxslt-dev libxml2 libxml2-dev \
  && apk add nginx supervisor


RUN addgroup -S django \
    && adduser -S -G django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

{%- if cookiecutter.use_celery == "y" %}
COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown django /start-celerybeat

COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower
{%- endif %}

{%- if cookiecutter.js_task_runner == 'Gulp' %}
COPY --from=client-builder /app /app
{% else %}
COPY . /app
{%- endif %}


# pai
COPY ./compose/production/supervisor/start-supervisor /start-supervisor
RUN sed -i 's/\r$//g' /start-supervisor
RUN chmod +x /start-supervisor

RUN mkdir -p /app/deploy
COPY ./compose/production/nginx/nginx.conf.template /app/deploy/
COPY ./compose/production/supervisor/supervisord.docker.conf /etc/supervisord.conf

RUN mkdir -p /var/log/supervisord/
RUN chmod a+rwx /var/log/supervisord
RUN chmod a+rw /etc/supervisord.conf

RUN chmod a+rw /etc/nginx/conf.d/default.conf

RUN mkdir -p /run/nginx


RUN chown -R django /app

USER root

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
