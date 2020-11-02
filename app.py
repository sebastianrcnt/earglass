from flask import Flask, render_template
from controllers import users, admin

app = Flask(__name__, template_folder="views")
app.secret_key = "earglass"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Blueprint
app.register_blueprint(users.controller, url_prefix="/users")
app.register_blueprint(admin.admin_bp)


# run
app.run(port=8080, host="0.0.0.0", debug=True)
