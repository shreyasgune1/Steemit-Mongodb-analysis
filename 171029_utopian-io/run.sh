#!/bin/bash

CONTAINER="utopian-post-analysis"

mkdir -p steemdata
docker build -t ${CONTAINER} .
docker run -v $PWD/steemdata:/steemdata ${CONTAINER}
