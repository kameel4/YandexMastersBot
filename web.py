import flask
import os

app = flask.Flask(__name__)


@app.route("/")
def school():
    return flask.render_template("sait.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
