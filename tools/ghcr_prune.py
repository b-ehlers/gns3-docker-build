#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (C) 2022 Bernhard Ehlers
# Copyright (C) 2021 Fiona Klute
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
ghcr_prune.py - Prune old versions of GHCR container.

Discussion:
https://github.community/t/are-tag-less-container-images-deleted/132977

Based on:
https://github.com/airtower-luna/hello-ghcr/blob/main/ghcr-prune.py

GitHub API Documentation:
https://docs.github.com/en/rest/reference/packages


usage: ghcr_prune.py [-h] [--dry-run] --prune-age DAYS
                     container [container ...]

positional arguments:
  container         images to prune

optional arguments:
  -h, --help        show this help message and exit
  --dry-run, -n     do not actually prune images, just list them
  --prune-age DAYS  delete untagged images older than DAYS days
"""

import os
import sys
import argparse
import json
import re
from datetime import datetime, timedelta
import dateutil.parser
import requests


parser = argparse.ArgumentParser(
             description='%(prog)s - Prune old versions of GHCR container.')
parser.add_argument('--dry-run', '-n', action='store_true',
                    help='do not actually prune images, just list them')
parser.add_argument('--prune-age', type=float, metavar='DAYS', required=True,
                    help='delete untagged images older than DAYS days')
parser.add_argument('container', nargs="+",
                    help='images to prune')

sess = requests.Session()
sess.headers.update({'Accept': 'application/vnd.github.v3+json'})


def container_prune(containers, prune_age, dry_run=False):
    """ prune old versions of GHCR container """

    # all: get names of all containers
    if len(containers) == 1 and containers[0] == "all":
        resp = sess.get('https://api.github.com/user/packages?'
                        'package_type=container')
        resp.raise_for_status()
        containers = sorted([pkg["name"] for pkg in json.loads(resp.content)])

    # prune each container
    for container in containers:
        print(f'Pruning images of {container}...')
        del_before = datetime.now().astimezone() - timedelta(days=prune_age)

        # get container versions
        resp = sess.get('https://api.github.com/user/packages/'
                        f'container/{container}/versions')
        resp.raise_for_status()
        versions = json.loads(resp.content)

        # store creation dates of tagged versions
        tagged_created = []
        for version in versions:
            if version["metadata"]["container"]["tags"]:
                tagged_created.append(
                    dateutil.parser.parse(version['created_at']))
        tag_window = timedelta(minutes=15)

        del_cnt = 0
        del_header = "Would delete" if dry_run else "Deleted"
        for version in sorted(versions, key=lambda k: k["id"], reverse=True):
            # prune old untagged images if requested
            created = dateutil.parser.parse(version['created_at'])
            if created < del_before and \
               not version["metadata"]["container"]["tags"]:
                # don't prune untagged images nearby tagged ones
                for tag_created in tagged_created:
                    if tag_created-tag_window < created <= tag_created:
                        break
                else:
                    if not dry_run:		# delete version
                        resp = sess.delete('https://api.github.com/user/packages/'
                                           f'container/{container}/'
                                           f'versions/{version["id"]}')
                        resp.raise_for_status()
                    if not del_cnt:
                        print(f'  {del_header}:')
                    print(f'  {version["name"]}')
                    del_cnt += 1


if __name__ == "__main__":
    args = parser.parse_args()

    if 'GHCR_TOKEN' in os.environ:
        token = os.environ['GHCR_TOKEN']
    else:
        sys.exit('missing authentication token (GHCR_TOKEN)')
    sess.headers.update({'Authorization': 'token ' + token})

    prog = os.path.basename(sys.argv[0])
    try:
        container_prune(args.container, args.prune_age, args.dry_run)
    except json.JSONDecodeError:
        sys.exit("{}: {}".format(prog, "Invalid JSON"))
    except (requests.exceptions.RequestException, ValueError) as err:
        msg = str(err)
        match = re.search(r"\(Caused by ([a-zA-Z0-9_]+)\('?[^:']*[:'] *(.*)'\)",
                          msg)
        if match:
            msg = match.group(2)
        sys.exit("{}: {}".format(prog, msg))
