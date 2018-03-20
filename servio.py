#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Fixed template url's
# Fixed api to accept code to return a 201 for post request
# Added requirements.txt
# Fixed minor styling

import os
import re
import six
import sys
import gzip
import json
import time
import socket
import jinja2
import sqlite3
import socketserver

from routes import Mapper
# from tabulate import tabulate
from http.server import BaseHTTPRequestHandler

env = jinja2.Environment(extensions=[])

FILETYPES = {
    '.a': 'application/octet-stream',
    '.ai': 'application/postscript',
    '.aif': 'audio/x-aiff',
    '.aifc': 'audio/x-aiff',
    '.aiff': 'audio/x-aiff',
    '.au': 'audio/basic',
    '.avi': 'video/x-msvideo',
    '.bat': 'text/plain',
    '.bcpio': 'application/x-bcpio',
    '.bin': 'application/octet-stream',
    '.bmp': 'image/x-ms-bmp',
    '.c': 'text/plain',
    '.cdf': 'application/x-netcdf',
    '.cpio': 'application/x-cpio',
    '.csh': 'application/x-csh',
    '.css': 'text/css',
    '.csv': 'text/csv',
    '.dll': 'application/octet-stream',
    '.doc': 'application/msword',
    '.dot': 'application/msword',
    '.dvi': 'application/x-dvi',
    '.eml': 'message/rfc822',
    '.eps': 'application/postscript',
    '.etx': 'text/x-setext',
    '.exe': 'application/octet-stream',
    '.gif': 'image/gif',
    '.gtar': 'application/x-gtar',
    '.h': 'text/plain',
    '.hdf': 'application/x-hdf',
    '.htm': 'text/html',
    '.html': 'text/html',
    '.ico': 'image/vnd.microsoft.icon',
    '.ief': 'image/ief',
    '.jpe': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.jpg': 'image/jpeg',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.ksh': 'text/plain',
    '.latex': 'application/x-latex',
    '.m1v': 'video/mpeg',
    '.m3u': 'application/vnd.apple.mpegurl',
    '.m3u8': 'application/vnd.apple.mpegurl',
    '.man': 'application/x-troff-man',
    '.map': 'application/octet-stream',
    '.me': 'application/x-troff-me',
    '.mht': 'message/rfc822',
    '.mhtml': 'message/rfc822',
    '.mif': 'application/x-mif',
    '.mov': 'video/quicktime',
    '.movie': 'video/x-sgi-movie',
    '.mp2': 'audio/mpeg',
    '.mp3': 'audio/mpeg',
    '.mp4': 'video/mp4',
    '.mpa': 'video/mpeg',
    '.mpe': 'video/mpeg',
    '.mpeg': 'video/mpeg',
    '.mpg': 'video/mpeg',
    '.ms': 'application/x-troff-ms',
    '.nc': 'application/x-netcdf',
    '.nws': 'message/rfc822',
    '.o': 'application/octet-stream',
    '.obj': 'application/octet-stream',
    '.oda': 'application/oda',
    '.p12': 'application/x-pkcs12',
    '.p7c': 'application/pkcs7-mime',
    '.pbm': 'image/x-portable-bitmap',
    '.pdf': 'application/pdf',
    '.pfx': 'application/x-pkcs12',
    '.pgm': 'image/x-portable-graymap',
    '.pl': 'text/plain',
    '.png': 'image/png',
    '.pnm': 'image/x-portable-anymap',
    '.pot': 'application/vnd.ms-powerpoint',
    '.ppa': 'application/vnd.ms-powerpoint',
    '.ppm': 'image/x-portable-pixmap',
    '.pps': 'application/vnd.ms-powerpoint',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.ps': 'application/postscript',
    '.pwz': 'application/vnd.ms-powerpoint',
    '.py': 'text/x-python',
    '.pyc': 'application/x-python-code',
    '.pyo': 'application/x-python-code',
    '.qt': 'video/quicktime',
    '.ra': 'audio/x-pn-realaudio',
    '.ram': 'application/x-pn-realaudio',
    '.ras': 'image/x-cmu-raster',
    '.rdf': 'application/xml',
    '.rgb': 'image/x-rgb',
    '.roff': 'application/x-troff',
    '.rtx': 'text/richtext',
    '.sgm': 'text/x-sgml',
    '.sgml': 'text/x-sgml',
    '.sh': 'application/x-sh',
    '.shar': 'application/x-shar',
    '.snd': 'audio/basic',
    '.so': 'application/octet-stream',
    '.src': 'application/x-wais-source',
    '.sv4cpio': 'application/x-sv4cpio',
    '.sv4crc': 'application/x-sv4crc',
    '.svg': 'image/svg+xml',
    '.swf': 'application/x-shockwave-flash',
    '.t': 'application/x-troff',
    '.tar': 'application/x-tar',
    '.tcl': 'application/x-tcl',
    '.tex': 'application/x-tex',
    '.texi': 'application/x-texinfo',
    '.texinfo': 'application/x-texinfo',
    '.tif': 'image/tiff',
    '.tiff': 'image/tiff',
    '.tr': 'application/x-troff',
    '.tsv': 'text/tab-separated-values',
    '.txt': 'text/plain',
    '.ustar': 'application/x-ustar',
    '.vcf': 'text/x-vcard',
    '.wav': 'audio/x-wav',
    '.webm': 'video/webm',
    '.wiz': 'application/msword',
    '.wsdl': 'application/xml',
    '.xbm': 'image/x-xbitmap',
    '.xlb': 'application/vnd.ms-excel',
    '.xls': 'application/vnd.ms-excel',
    '.xml': 'text/xml',
    '.xpdl': 'application/xml',
    '.xpm': 'image/x-xpixmap',
    '.xsl': 'application/xml',
    '.xwd': 'image/x-xwindowdump',
    '.zip': 'application/zip'}

class Headers:
    BaseHeaders = [
        ["Access-Control-Allow-Origin", "*"],
        ["Access-Control-Allow-Headers", "Content-Type"],
        ["Access-Control-Allow-Headers", "Content-Encoding"],
        ['Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT, DELETE']
    ]

    SecurityHeaders = [
        ["X-Frame-Options", "SAMEORIGIN"],
        ["X-XSS-Protection", "1"],
        ["X-Content-Type-Options", "nosniff"],
    ]

    FileHeaders = [
        ["Access-Control-Allow-Headers", "Content-Disposition"],
        ["Access-Control-Allow-Headers", "Content-Length"],
        ["Access-Control-Allow-Headers", "Filename"],
    ]

class HTTPServio(socketserver.TCPServer):

    allow_reuse_address = 1    # Seems to make sense in testing environment

    def __init__(self, *args):
        self.map = Mapper()
        print("["+time.asctime()+"] Server Starts "+''.join(str(args[0])))
        socketserver.TCPServer.__init__(self, *args)

    def route(self, path, methods):
        def decorator(f):
            self.map.connect(path, controller=f, conditions={"method": methods})
            return f
        return decorator

    def get_route_match(self, path, command):
        environ = {
            'PATH_INFO': path,
            'REQUEST_METHOD': command
        }

        resource = self.map.match(environ=environ)
        if resource:
            return resource, resource['controller']

        return None

    def serve(self, path, command):
        route_match = self.get_route_match(path, command)

        if route_match:
            kwargs, view_function = route_match
            return view_function, kwargs
        else:
            return None, None

    def server_bind(self):
        """Override server_bind to store the server name."""
        try:
            socketserver.TCPServer.server_bind(self)
            host, port = self.server_address[:2]
            self.server_name = socket.getfqdn(host)
            self.server_port = port
        except OSERROR:
            print("Address in use")
            sys.exit(0)

    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        return

class Servio(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        return

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
                    self.send_error("Not implemented.")
                    return
                method = getattr(self, mname)
                method()
            self.wfile.flush()

        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return

    def isFilePath(self, content):
        if content == "/":
            content = "/index.html"
            return True

        if os.path.isfile(os.curdir + os.sep + content):
            return True
        return False

    def api(self, code, content):
        self.send_response(code)
        self.send_header('Content-type', "application/json")
        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        self.end_headers()
        self.wfile.write(bytes(json.dumps(content).encode("utf-8")))
        return

    def apifailure(self):
        self.send_response(404)
        self.send_header('Content-type', "application/json")
        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        self.end_headers()
        self.wfile.write(bytes(json.dumps({"Failure": "Generic Failure"}).encode("utf-8")))

    def html(self, content="<h1>Test</h1>"):
        self.send_response(200)

        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.SecurityHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.FileHeaders]

        if self.isFilePath(content) and content != "/":
            upperpath, bottompath = os.path.splitext(content)

            try:
                mimetype = FILETYPES[bottompath]
            except KeyError:
                mimetype = "text/plain"

            with open(os.curdir + os.sep + content, 'rb') as fh:
                content = gzipencode(fh.read())

        else:
            content = gzipencode(bytes(content.encode('utf-8')))
            mimetype = "text/html"

        self.send_header('Content-type', mimetype)
        self.send_header("Content-length", str(len(str(content))))
        self.send_header("Content-Encoding", "gzip")

        self.end_headers()
        self.wfile.write(content)
        self.wfile.flush()

        return

    def download(self, name):
        upperpath, bottompath = os.path.splitext(name)
        mimetype = FILETYPES[bottompath]

        self.send_response(200)
        self.send_header('Content-type', mimetype)
        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.SecurityHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.FileHeaders]
        self.send_header("Content-Disposition", "attachment; filename={0}".format(name))

        with open("files/"+name, 'rb') as fh:
            content = gzipencode(fh.read())
            self.send_header("Content-length", str(len(str(content))))
            self.send_header("Content-Encoding", "gzip")
            self.end_headers()
            self.wfile.write(bytes(content))
            self.wfile.flush()
        return

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

    def template(self, path, context):
        self.send_response(200)
        if not path.endswith(".jinja"):
            path += ".jinja"

        if not path.startswith("/templates/"):
            path = "templates"+path

        if context:
            env.globals.update(context)

        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.SecurityHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.FileHeaders]

        self.send_header('Content-type', "text/html")
        self.send_header("Content-Encoding", "gzip")

        with open(path, "rb") as fh:
            template = env.from_string(fh.read().decode('utf-8')).render().encode('utf-8')

        self.send_header("Content-length", str(len(str(template))))
        self.end_headers()

        self.wfile.write(gzipencode(bytes(template)))
        self.wfile.flush()

    def do_GET(self):
        if self.isFilePath(self.path):

            if self.path.endswith(".jinja"):
                self.template(self.path, None)
            else:
                self.html(self.path)

        else:

            if self.path.endswith(".jinja"):
                self.template(self.path, None)
            else:
                self.error404()

        return

    def do_OPTIONS(self):
        self.send_response(200, "ok")

        [self.send_header(header[0], header[1]) for header in Headers.BaseHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.SecurityHeaders]
        [self.send_header(header[0], header[1]) for header in Headers.FileHeaders]

        self.end_headers()
        return

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
