#! /usr/bin/env python

import argparse
import json
import logging
import os
import random
import typing

from atproto import Client


class FortuneBot(object):
    fortunes: list[str] | None = None

    def __init__(self, datadir=".", files=[]):
        self.fortunes = self.read_fortunes(files=files, datadir=datadir)

    def read_fortunes(self, files: list[str], datadir="./data") -> list[str]:
        fortunes = []
        for fname in files:
            with open(f"{datadir}/{fname}", "r") as f:
                for fortune in self.delimited_read(f, "\n%\n"):
                    if len(fortune) > 300:
                        logging.warning(
                            'Quote too long (%d chars): "%s..."',
                            len(fortune),
                            fortune[0:50]
                        )
                    else:
                        fortunes.append(fortune)
        return fortunes

    def choose_fortune(self) -> str:
        return random.choice(self.fortunes)

    def delimited_read(self, file_handle, delimiter='\n', bufsize=4096):
        buf = ''
        while True:
            newbuf = file_handle.read(bufsize)
            if not newbuf:
                yield buf
                return
            buf += newbuf
            lines = buf.split(delimiter)
            for line in lines[:-1]:
                yield line
            buf = lines[-1]



def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', type=str, default='INFO')
    parser.add_argument('-n', '--dry-run', action='store_true')
    args = parser.parse_args()

    # Config
    with open("config.json", "r") as f:
        cfg = json.load(f)

    # Initialize log level
    os.makedirs(cfg["log_dir"], exist_ok=True)
    logging.basicConfig(
        filename=f"{cfg['log_dir']}/plumbot.log",
        level=args.loglevel,
        format="%(asctime)s %(message)s"
    )

    # Read and post a fortune
    bot = FortuneBot(datadir=cfg["fortune_dir"], files=cfg["fortune_files"])
    logging.debug("read %d fortunes", len(bot.fortunes))
    fortune = bot.choose_fortune()

    client = Client()
    client.login(cfg["bsky_username"], cfg["bsky_password"])
    if args.dry_run:
        print(f"Snippet: {fortune}")
    else:
        client.send_post(text=fortune)


if __name__ == "__main__":
    main()

