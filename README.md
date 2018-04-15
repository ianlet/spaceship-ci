# CS Games ULaval 2018 - Spaceship CI

Continuous integration tool that will fetch github repositories from an organization in order to continuously build,
test and track their progress.

## Requirements

- python 3.6
- pip
- docker

## Installation

```
pip install -r requirements.txt
```

## Configuration

You must store your github token in the `GITHUB_TOKEN` environment variables as well the mongo host and port in the
`MONGO_HOST` and `MONGO_PORT` environment variables.

You also have to provide a database name with the `SPACESHIP_DATABASE` environment variable.

## Usage

Make sure Docker and MongoDB are up and running and execute the following command:

```
python main.py -o [ORG_NAME] -c [CHALLENGE_NAME]
```

Where `ORG_NAME` is the Github organization where the repositories are stored and `CHALLENGE_NAME` is the prefix
every repository you want to continuously integrate should have.

For example, with the following command:

```
python main.py -o csgames-ulaval -c team-software-engineering
```

The spaceship-ci will fetch and run every projects in the `csgames-ulaval` organization starting with
`team-software-engineering`.
