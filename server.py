#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from servio import *

app = HTTPServio(('0.0.0.0', 8080), Servio)

class DBCON(ServioQL):

    def list_posts(self):
        self.cursor.execute("SELECT * FROM posts")
        return self.cursor.fetchall()

    def retrieve_post(self, post_id):
        self.cursor.execute("SELECT * FROM posts WHERE id=(?)", [post_id])
        return self.cursor.fetchone()

@app.route("/", methods=["GET"])
def index(srv, **kwargs):
    srv.html("index.html")
    return

@app.route("/posts", methods=["GET"])
def index(srv, **kwargs):
    dbc = DBCON("test.db")
    srv.api(200, dbc.list_posts())
    return

@app.route("/posts/{id}", methods=["GET"])
def index(srv, **kwargs):
    dbc = DBCON("test.db")
    content = dbc.retrieve_post(kwargs['id'])
    if content:
        srv.api(200, content)
    else:
        srv.apifailure()
    return

app.run()
