#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from RESvio import *

app = HTTPServio(('0.0.0.0', 8081), Servio)

@app.route("/", methods=["GET"])
def index(srv, **kwargs):
    srv.api(200, "GET")
    return

@app.route("/", methods=["POST"])
def index(srv, **kwargs):
    srv.api(200, "POST")
    return

app.run()
