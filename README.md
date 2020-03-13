# shipwreck / weathervane

Gather diagnostic information from third party providers for use during incidents and diagnostic operations.

Meant to assist when running incidents to save some time and aggregate statuses of major providers.

## Requirements

The tool requires Python 3.

Run `pip3 install -r requirements.txt` to install dependencies.

## Current Provider Compatibility

* Heroku
* GitHub

## Usage

The tool can be invoked via the command line and has various options that can be passed in:

```bash
usage: wv.py [-h] [-p PROVIDERS]

Gather diagnostic information from third party providers for use during
incidents and diagnostic operations.

optional arguments:
  -h, --help            show this help message and exit
  -p PROVIDERS, --providers PROVIDERS
                        Comma separated list of providers to get reports from.
                        Options are: heroku, github
```

### Sample CLI Usage

`python3 wv.py -p github, heroku` - gather details on Heroku and GitHub.

## Running in Docker

Alternatively, you can run the tool using Docker, passing arguments the same way:

`docker container run shipwreckdev/weathervane -p github`

This makes it easy to use the tool in automation or pipelines where Docker is available.

## Update Paths

More providers will be added in the future.
