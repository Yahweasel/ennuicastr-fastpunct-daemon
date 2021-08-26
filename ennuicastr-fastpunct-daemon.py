#!/usr/bin/env python3
# Copyright (c) 2021 Yahweasel
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import json
import os
import socketserver

from nnsplit import NNSplit
from fastpunct import FastPunct

# Do some pre-punctuation just to prime the pump
splitter = NNSplit.load("en")
fastpunct = FastPunct()
fastpunct.punct(
    list(map(str, splitter.split(["john smiths dog is creating a ruccus " +
    "ys jagan is the chief minister of andhra pradesh " +
    "we visted new york last year in may"])[0]))
)

# Get the server socket
addr = "/tmp/ennuicastr-fastpunct-daemon.sock"
try:
    os.unlink(addr)
except OSError:
    pass

# Segmenter-punctuator
def punctuate(line):
    return " ".join(
        fastpunct.punct(
            list(map(str,
                splitter.split([line])[0]
            ))
        )
    )

# Main server
class FastPunctDaemonReqHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            # Expected format is one JSON object per line
            line = self.rfile.readline()
            if line == "":
                break

            try:
                obj = json.loads(line)
                # Expected format: {"c":"fastpunct","i":[array of strings]}
                res = list(map(punctuate, obj["i"]))
                # Return format: {"o":[result]}
                ress = json.dumps({
                    "o": res
                })
                self.wfile.write(bytes(ress + "\n", "utf8"))
            except Exception:
                break

class FastPunctDaemonServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    pass

server = FastPunctDaemonServer(addr, FastPunctDaemonReqHandler)
server.serve_forever()
