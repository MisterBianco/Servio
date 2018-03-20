#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import six
import sys
import gzip
import json
import time
import socket
import sqlite3
import socketserver

from routes import Mapper
from http.server import BaseHTTPRequestHandler

class Headers:
    BaseHeaders = [
        ["Access-Control-Allow-Origin", "*"],
        ["Access-Control-Allow-Headers", "Content-Type"],
        ["Access-Control-Allow-Headers", "Content-Encoding"],
        ['Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT, DELETE']
    ]

    SecurityHeaders = [
        ["X-XSS-Protection", "1"],
        ["X-Frame-Options", "SAMEORIGIN"],
        ["X-Content-Type-Options", "nosniff"],
    ]

    FileHeaders = [
        ["Access-Control-Allow-Headers", "Content-Disposition"],
        ["Access-Control-Allow-Headers", "Content-Length"],
    ]

class HTTPServio(socketserver.TCPServer):

    def __init__(self, *args):
        self.map = Mapper()
        print("["+time.asctime()+"] Server Starts "+''.join(str(args[0])))
        socketserver.TCPServer.__init__(self, *args)

    def route(self, path, methods):
        def decorator(f):
            self.map.connect(path, controller=f, conditions={"method": methods})
            return f
        return decorator

    def cache(self, path):
        pass

    def get_route_match(self, path, command):
        environ = {
            'PATH_INFO': path,
            'REQUEST_METHOD': command}

        resource = self.map.match(environ=environ)
        if resource:
            return resource, resource['controller']

        return None, None

    def serve(self, path, command):
        controller, resource = self.get_route_match(path, command)
        return resource, controller

    def server_bind(self):
        """Override server_bind to store the server name."""
        try:
            socketserver.TCPServer.server_bind(self)
            host, port = self.server_address[:2]
            self.server_name = socket.getfqdn(host)
            self.server_port = port
        except Exception as e:
            print(e)
            sys.exit(0)

    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        return

class Servio(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.server_version = "Resvio 1.0.0"
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        return

    def log_message(self, format, *args):
        try:
            print("["+time.asctime()+"] {0}:[{3}] {1} -> {2}".format(
                self.command,
                self.client_address[0],
                self.headers["User-Agent"],
                self.path)
            )
        except:
            pass
        return

    def version_string(self):
        return self.server_version

    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return

            if not self.raw_requestline:
                self.close_connection = True
                return

            if not self.parse_request():
                # An error code has been sent, just exit
                return

            function, kwargs = self.server.serve(self.path, self.command)
            if function:
                function(self, **kwargs)

            else:
                mname = 'do_' + self.command
                if not hasattr(self, mname):
                    self.send_error(400)
                    return
                method = getattr(self, mname)
                method()
            self.wfile.flush()

        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return

    def api(self, code, content):
        self.send_response(code)
        self.send_header('Content-type', "application/json")
        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.SecurityHeaders]
        self.end_headers()
        self.wfile.write(bytes(json.dumps(content).encode("utf-8")))
        return

    def apifailure(self):
        self.send_response(404)
        self.send_header('Content-type', "application/json")
        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.SecurityHeaders]
        self.end_headers()
        self.wfile.write(bytes(json.dumps({"Failure": "Generic Failure"}).encode("utf-8")))

    def error404(self):
        self.send_response(404)
        self.send_header('Content-type', "text/html")
        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.SecurityHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.FileHeaders]

        content = gzipencode(b"Error: 404<br>Not Found")
        self.send_header("Content-length", str(len(str(content))))
        self.send_header("Content-Encoding", "gzip")
        self.end_headers()
        self.wfile.write(content)
        self.wfile.flush()

        return

    def do_OPTIONS(self):
        self.send_response(200, "ok")

        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.SecurityHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.FileHeaders]

        self.end_headers()
        return

    def do_GET(self):
        self.error404()

    def do_POST(self):
        self.error404()

    def do_DELETE(self):
        self.error404()

    def do_PUT(self):
        self.error404()

class ServioQL:

    def __init__(self, dbfile, foreign_keys=False):
        self.connection = sqlite3.connect(dbfile)
        self.connection.row_factory = dictFactory
        self.cursor = self.connection.cursor()

        if foreign_keys:
            self.cursor.execute("PRAGMA foreign_keys = ON")
        return

    def __del__(self):
        self.connection.close()
        return

    def listTables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cursor.fetchall()

    def clean(self):
        for table in self.listTables():
            self.cursor.execute("DELETE FROM "+table['name'])
            self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='{0}'".format(table['name']))
            self.connection.commit()
        return

def gzipencode(content):
    out = six.BytesIO()
    f = gzip.GzipFile(fileobj=out, mode='w', compresslevel=5)
    f.write(content)
    f.close()
    return out.getvalue()

def dictFactory(cursor, row):
    return {value[0]: row[key] for (key, value) in enumerate(cursor.description)}
