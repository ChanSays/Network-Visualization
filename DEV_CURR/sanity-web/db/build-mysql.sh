#!/usr/bin/env bash
docker build . -t containers.cisco.com/jonali/sanity-db && \
docker push containers.cisco.com/jonali/sanity-db:latest