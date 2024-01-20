# build stage
FROM python:3.11.2-alpine3.17 AS build

WORKDIR /usr/src/app

RUN apk add --no-cache gcc musl-dev \
    && rm -rf /var/cache/apk/*

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt && \
    find /root/.local/ -depth \
        \( \
            \( -type d -a -name test -o -name tests \) \
            -o \
            \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        \) -exec rm -rf '{}' +

# final stage
FROM python:3.11.2-alpine3.17

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"

ARG GROUP_ID
ARG USER_ID

# create an app user
RUN addgroup --gid $GROUP_ID appuser && \
    adduser --uid $USER_ID --ingroup appuser --home /home/appuser --shell /bin/sh --disabled-password appuser

COPY --from=build /root/.local /home/appuser/.local
COPY . .



# chown all the files to the app user
RUN chown -R appuser:appuser /usr/src/app && \
    chmod -R u+w /usr/src/app



# switch to the app user
USER appuser
