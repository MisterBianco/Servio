#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from servio import *

app = HTTPServio(('0.0.0.0', 8080), Servio)

class DBCON(ServioQL):

    def getfiles(self, name):
        self.cursor.execute("SELECT * FROM files WHERE filename=?", [name])
        return self.cursor.fetchone()

@app.route("/", methods=["GET"])
def index(srv, **kwargs):
    srv.html("index.html")
    return

@app.route("/{name}", methods=["GET"])
def index(srv, **kwargs):
    db = DBCON("test.db")
    files = db.getfiles(kwargs['name'])
    print(files)
    srv.api(files)
    return

app.run()
