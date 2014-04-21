# This file is part of ZSS
# Copyright (C) 2013-2014 Nathaniel Smith <njs@pobox.com>
# See file LICENSE.txt for license information.

import sys
import binascii
from collections import OrderedDict

import json
from .util import open_zss

def command_info(opts):
    """Display general information from a .zss file's header.

Usage:
  zss info [--metadata-only] [--] <zss_file>
  zss info --help

Arguments:
  <zss_file>  Path or URL pointing to a .zss file. An argument beginning with
              the four characters "http" will be treated as a URL.

Options:
  -m, --metadata-only   Output only the file's metadata, not any general
                        information about it.

Output will be valid JSON.
"""

    with open_zss(opts) as z:
        if opts["--metadata-only"]:
            info = z.metadata
        else:
            info = OrderedDict()
            info["root_index_offset"] = z.root_index_offset
            info["root_index_length"] = z.root_index_length
            info["total_file_length"] = z.total_file_length
            info["codec"] = z.codec
            info["data_sha256"] = (binascii.hexlify(z.data_sha256)
                                   .decode("ascii"))
            info["metadata"] = z.metadata
            info["statistics"] = OrderedDict()
            info["statistics"]["root_index_level"] = z.root_index_level
        json.dump(info, sys.stdout, indent=4)
        sys.stdout.write("\n")

    return 0
