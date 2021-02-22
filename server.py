""" Queue-writer
    server.py:      Simple Flask+connexion server. Provides REST endpoint to enqueue messages
    message.py:     Handlers for /message REST calls.
    swagger.yml:    OpenAPI definition
"""

import connexion
from flask import render_template

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml", options={"swagger_ui": False})


@app.route("/")
def home():
    """ Render page with link to Swagger UI
        The page can be used as health monitoring target
    """
    return render_template("default.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
