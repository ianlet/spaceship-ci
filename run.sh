#! /bin/sh

organization="$1"
challenge="$2"

GITHUB_TOKEN=57cb38766e2432661eb08ab278110b8ada040dae \
  MONGO_HOST=localhost \
  MONGO_PORT=27017 \
  SPACESHIP_DATABASE=spaceship \
  python ~/projects/csgames/challenges/tse/spaceship-ci/main.py -o $organization -c $challenge
