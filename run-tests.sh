
#!/bin/bash
set -e

echo "##########################################"
echo "Building unit tests"
echo "##########################################"
docker compose -f docker-compose-unit-tests.yml build

echo "##########################################"
echo "Running unit tests"
echo "##########################################"
docker compose -f docker-compose-unit-tests.yml up \
  --force-recreate \
  --remove-orphans \
  --no-log-prefix \
  --abort-on-container-exit \
  --exit-code-from tests