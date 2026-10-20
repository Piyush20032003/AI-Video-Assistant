#!/bin/bash
set -e

apt-get update
apt-get install -y ffmpeg unzip curl

curl -fsSL https://deno.land/install.sh | sh

export DENO_INSTALL="/root/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"

deno --version
