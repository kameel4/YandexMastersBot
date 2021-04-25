import flask

app = flask.Flask(__name__)


@app.route("/")
def school():
    return flask.render_template("sait.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
