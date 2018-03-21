#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from servio import *

app = HTTPServio(('0.0.0.0', 8080), Servio)

@app.route("/get", methods=["GET"])
def index(srv, **kwargs):
    srv.api(200, "GET")
    return

@app.route("/post", methods=["POST"])
def index(srv, **kwargs):
    srv.api(200, "POST")
    return

app.run()
