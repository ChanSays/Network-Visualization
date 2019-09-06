#!/sh/env bash
docker build . -f Dockerfile.prod -t containers.cisco.com/jonali/sanity-web && \
docker push containers.cisco.com/jonali/sanity-web:latest