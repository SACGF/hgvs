#################################################################################
# STAGE - BUILD
#################################################################################
FROM python:3.10-slim as build

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements.txt
COPY . /app

#################################################################################
# STAGE - TESTS
#################################################################################
FROM build as tests
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements-dev.txt

#################################################################################
# STAGE - RUNTIME
#################################################################################
FROM python:3.10-slim AS runtime
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=build /app /app
COPY --from=build /usr/local /usr/local
CMD ["uvicorn", "pyhgvs.api:app", "--host", "0.0.0.0", "--port", "8002"]