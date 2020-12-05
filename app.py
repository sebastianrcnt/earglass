from flask import Flask, render_template, request, redirect
from controllers import users, admin, task, submitter, estimator
from werkzeug.wrappers import Request
import services
from settings import as_json
import os



app = Flask(__name__, template_folder="templates")
app.secret_key = "earglass"
app.config['JSON_AS_ASCII'] = False

@app.context_processor
def inject_user():
    def is_logged_in():
        user_id = request.cookies.get("user_id")
        user = services.users.get_user_by_id(user_id)
        if user: return user
        else: return False

    def is_submitter():
        user_id = request.cookies.get("user_id")
        user = services.users.get_user_by_id(user_id)
        if user["FK_UserTypeName"] == "제출자" : return user
        else: return False

    def is_estimator():
        user_id = request.cookies.get("user_id")
        user = services.users.get_user_by_id(user_id)
        if user["FK_UserTypeName"] == "평가자": return user
        else: return False
# 관리자 추가 필요 (규식)
    def is_admin():
        user_id = request.cookies.get("user_id")
        user = services.users.get_user_by_id(user_id)
        if user["FK_UserTypeName"] == "관리자": return user
        else: return False

    return dict(is_logged_in=is_logged_in, is_submitter=is_submitter, is_estimator=is_estimator)


@app.route("/", methods=["GET"])
def index():
    user_id = request.cookies.get("user_id")
    user = services.users.get_user_by_id(user_id)
    if user:
        # admin:
        if user["FK_UserTypeName"] == "관리자":
            return redirect("/admin")

        # submitter:
        if user["FK_UserTypeName"] == "제출자":
            return redirect("/submitter")

        # estimator:
        if user["FK_UserTypeName"] == "평가자":
            return redirect("/estimator")
    else:
        return render_template("index.html")

# Blueprint(Routers)
app.register_blueprint(users.controller, url_prefix="/users")
app.register_blueprint(admin.controller, url_prefix="/admin")
app.register_blueprint(task.controller, url_prefix="/task")
app.register_blueprint(submitter.controller, url_prefix="/submitter")
app.register_blueprint(estimator.controller, url_prefix="/estimator")


# run
app.run(port=8080, host="0.0.0.0", debug=True)
