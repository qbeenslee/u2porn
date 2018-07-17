#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
R_DIR="$(dirname "$(readlink -n "$0")")"
cd "$DIR/$R_DIR"
scrapy crawl u2porn -a title=$1
