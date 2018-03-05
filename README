Servio
=====

An advanced httpserver built on the standard http.server in __python3__ that
GZIP's all data.

Servio is easy to use and is designed to mimic more advanced servers like
_flask_ or _django_

Stability: Testing

---

The usage is simple:
--

```
    from servio import *
    app = HTTPServio(('0.0.0.0', 8080), Servio)

    @app.route("/", methods=["GET"])
    def index(srv, **kwargs):
        srv.api("Success")
        return

    app.run()
```

The above defines a URL mapping to the "/" and returns a json object containing
"Success." However the server can also return html or a template object.

The templating is using jinja2 so any previously portable code for jinja will
work here.

---

The server supports:
--
+ API objects with the: srv.api()
+ HTML with the: srv.html("_PATH_TO\_FILE_")
+ Templates with: srv.tempalte("_PATH_TO\_TEMPLATE_")

---
SQLITE3
--

If you plan on using SQLITE3 this library has its own sqlite3 wrapper that adds
some nice functions to databases.

Examples:
+ dbobject.clean()
    - Cleans all objects from all tables for a brand new clean db.
+ dbobject.listTables()
    - Lists all tables in a database.

---

Additional Usage:
--

API call to return a part of the url on post:
```
    @app.route("/api/{action}", methods=["POST"])
    def api_action(srv, **kwargs):
        srv.api(kwargs['action'])
        return
```

Passing a chunk of the url to a template on post:

```
    @app.route("/api/{action}/{descriptor}", methods=["POST"])
    def api_action(srv, **kwargs):
        srv.template("index", {"User": kwargs['action']})
        # srv.api({"resource": kwargs['action'], "item": kwargs['descriptor']})
        return
```

Serving HTML on a qualified path:

```
    @app.route("/index", methods=["GET"])
    def index(srv, **kwargs):
        srv.html("index.html")
        return
```

---

I don't necessarily recommend using this unless you are required to use the
python builtin http.server and in that case you can use this just fine.

Really it's meant to be a helpful library for the Dixie State CS3200 class
students.

---
