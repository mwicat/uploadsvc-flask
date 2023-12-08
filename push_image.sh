#!/bin/bash

set -Eeuo pipefail

docker build . -t mwicat/uploadsvc
docker push mwicat/uploadsvc
