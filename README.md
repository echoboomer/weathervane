# shipwreck / weathervane

![weathervane](https://github.com/shipwreckdev/weathervane/blob/master/assets/wv.png)

Weathervane allows a team to gather diagnostic information from third party providers in one place.

The tool was built to assist when running incidents to save some time and aggregate statuses of major providers.

This comes in handy when service interruptions are occurring. A handy way to implement the tool is to have incident bots run it at the beginning of incident channels.

## Requirements

* `python3`

## Current Provider Compatibility

* GitHub
* Heroku

## Usage

The tool can be cloned from this repository and run locally:

* `git clone https://github.com/shipwreckdev/weathervane.git`
* `pip3 install -r requirements.txt`

The tool can then be invoked via the command line and has various arguments that can be passed in.

To get a quick overview of arguments, run `python3 wv.py -h`:

```bash
usage: wv.py [-h] [-p PROVIDERS] [-c]

Gather diagnostic information from third party providers for use during
incidents and diagnostic operations.

optional arguments:
  -h, --help            show this help message and exit
  -p PROVIDERS, --providers PROVIDERS
                        Comma separated list of providers to get reports from.
                        Options are: heroku, github
  -c, --compact         Show compact summary instead of verbose output.
                        Ignores incident details and header.
```

Passing in the `-c` flag suppresses incident details and removes the header. This is the more useful option if minimal output is required with only a brief statement on service availability.

### Sample CLI Usage

* `python3 wv.py -p github,heroku` - gather details on Heroku and GitHub.
* `python3 wv.py -p github,heroku -c` - gather details on Heroku and GitHub, but skip provider incident information.

## Running in Docker

Alternatively, you can run the tool using Docker, passing in arguments the same way:

`docker container run shipwreckdev/weathervane -p github,heroku -c`

This makes it easy to use the tool in automation or pipelines where Docker is available, and also avoids the need to clone the repository down locally.

## Future Updates

* More providers will be added to the tool.
* Base APIs are hardcoded into the tool. These could theoretically change, so the ability to override base APIs will be introduced.
