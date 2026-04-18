# plumbot

plumbot - a simple quotes bot for Bluesky.

## Description

Plumbot reads files in the traditional Unix fortune(5) format, selects a fortune at random, and posts it to the specified Bluesky account.

    -l, --loglevel=LEVEL     Log messages at the specified syslog LEVEL.

    -n, --dry-run            Do not post anything, but print to stdout what would have been posted.

## Configuration

Plumbot is configured by way of a `config.json` file in the working directory with the following settings:

```
{
  "fortune_dir": "...",
  "fortune_files": [
    "...",
  ],
  "log_dir": "...",
  "bsky_username": "username.bsky.social",
  "bsky_password": "squamous!ossifrage"
}
```

* `fortune_dir` is a directory to where fortune files are kept.
* `fortune_files` is a list of filenames found within `fortune_dir`.
* `log_dir` is the directory where logs are written.
* `bsky_username` and `bsky_password` are credentials for posting to Bluesky.

