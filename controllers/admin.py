from flask import Blueprint, render_template, redirect, request, make_response, flash
import services
from database.connection import queryall, queryone

# writed by seungsu

controller = Blueprint("admin", __name__)

# /
@controller.route("/", methods=["GET"])
def get_admin_page():
    tasks = services.admin.get_all_tasks()

    # 제출자들이 참여하는 태스크 목록
    submitters = queryall("SELECT * FROM USER WHERE FK_UserTypeName = '제출자'")
    for submitter in submitters:
        user_index = submitter['idUSER']
        participating_tasks = queryall("SELECT FK_TaskName FROM PARTICIPATION WHERE FK_idUSER=%s AND Status = 'ongoing'", (user_index, ))
        submitter['Tasks'] = participating_tasks

    # 평가자들이 참여하는 태스크 목록
    estimators = queryall("SELECT * FROM USER WHERE FK_UserTypeName = '평가자'")
    for estimator in estimators:
        user_index = estimator['idUSER']
        participating_tasks = queryall("SELECT P.TaskName FROM EVALUATION AS E  \
            LEFT JOIN PARSING_DSF AS P ON E.FK_idPARSING_DSF = P.idPARSING_DSF WHERE E.FK_idEstimator=%s AND E.Status = 'ongoing' " , (user_index, ))
        estimator['Tasks'] = participating_tasks

    users = submitters + estimators
    return render_template("admin/index.html", users=users, tasks=tasks)

# TASK
# /task
@controller.route("/add_task", methods=["GET"])
def get_add_task_page():
    '''태스크 추가 페이지'''
    return render_template("admin/add_task.html")

@controller.route("/tasks/<task_name>", methods=["GET"])
def get_task_page(task_name):
    '''태스크 상세/수정 페이지'''
    task = services.admin.task_info(task_name)
    origin_data_types = services.admin.task_info_origin_data_type(task_name)
    task_participation = services.admin.show_task_participation_list(task_name)

    return render_template("admin/task_info.html", task=task, origin_data_types=origin_data_types, task_participation=task_participation)

@controller.route("/tasks", methods=["POST"])
def add_task():
    '''태스크 추가 엔드포인트'''
    task_name = request.form.get("task_name")
    description = request.form.get("description")
    min_period = request.form.get("min_period")
    status = request.form.get("status")
    task_data_table_name = request.form.get("task_data_table_name")
    deadline = request.form.get("deadline")
    max_duplicated_row_ratio = request.form.get("max_duplicated_row_ratio")
    max_null_ratio_per_column = request.form.get("max_null_ratio_per_column")
    pass_criteria = request.form.get("pass_criteria")

    services.admin.add_task(task_name, description, min_period, status, task_data_table_name, deadline, max_duplicated_row_ratio, max_null_ratio_per_column, pass_criteria)
    # TODO add task
    return "Uncompleted"

@controller.route("/tasks/<task_name>", methods=["POST"])
def edit_task(task_name):
    '''태스크 수정 엔드포인트'''
    # TODO edit task
    return "Uncompleted"

@controller.route("/tasks", methods=["DELETE"])
def delete_task():
    '''태스크 삭제 엔드포인트'''
    # TODO delete task
    return "Uncompleted"


# USERS
# /user
@controller.route("/submitters/<submitter_index>", methods=["GET"])
def get_admin_submitter_page(submitter_index):
    user = services.users.get_user_by_index(submitter_index)
    participations = services.submitter.participating_tasklist(submitter_index)
    if not user:
        flash("해당 id에 대한 유저가 존재하지 않습니다")
        return redirect("/admin/")

    return render_template("admin/submitter.html", user=user, participations=participations)

@controller.route("/estimators/<estimator_index>", methods=["GET"])
def get_admin_estimator_page(estimator_index):
    # TODO estimator detail page
    return render_template("admin/estimator.html")
# Create Read Update Delete(CRUD)

