from flask import Blueprint, render_template, redirect, request, make_response, flash
from services import admin

# writed by seungsu

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/", methods=["GET"])
def get_main_admin():
    return render_template()


@admin_bp.route("/submitter/<int:user_id>", methods=["GET"])
def get_detail_submitter(user_id):
    return render_template()


@admin_bp.route("/estimator/<int:user_id>", methods=["GET"])
def get_detail_estimator(user_id):
    return render_template()


@admin_bp.route("/task", methods=("POST", "PUT"))
def task():
    # task 추가
    if request.method == "POST":
        pass

    # task 수정
    elif request.method == "PUT":
        pass

    return render_template()


@admin_bp.route("/task/<int:task_id>", methods=["GET"])
def detail_task(task_id):
    # show task detail
    return render_template()
