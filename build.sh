#/bin/bash

set -o errexit
set -o nounset
set -o pipefail

IMAGE=oneway_clipboard
RELEASE="0.0.1" 
CONTAINER=oneway_clipboard

docker buildx build -t $IMAGE:$RELEASE .
docker save -o $IMAGE"_"$RELEASE".tar" $IMAGE:$RELEASE

