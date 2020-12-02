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
        participating_tasks = queryall(
            "SELECT FK_TaskName FROM PARTICIPATION WHERE FK_idUSER=%s AND Status = 'ongoing'", (user_index, ))
        submitter['Tasks'] = participating_tasks

    # 평가자들이 참여하는 태스크 목록
    estimators = queryall("SELECT * FROM USER WHERE FK_UserTypeName = '평가자'")
    for estimator in estimators:
        user_index = estimator['idUSER']
        participating_tasks = queryall("SELECT P.TaskName FROM EVALUATION AS E  \
            LEFT JOIN PARSING_DSF AS P ON E.FK_idPARSING_DSF = P.idPARSING_DSF WHERE E.FK_idEstimator=%s AND E.Status = 'ongoing' ", (user_index, ))
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
    '''태스크 상세페이지'''
    task = services.admin.task_info(task_name)
    origin_data_types = services.admin.task_info_origin_data_type(task_name)
    print(origin_data_types)
    task_participation = services.admin.show_task_participation_list(task_name)

    return render_template("admin/task_info.html", task=task, origin_data_types=origin_data_types, task_participation=task_participation)


@controller.route("/tasks/agreement", methods=["GET"])
def confirm_agreement():
    """
    태스크 참여 신청 처리
    """
    # TODO 관리자인지 확인 필요

    print(request.args)
    user_id = request.args.get('user_id', False)
    user_index = services.users.get_user_by_id(user_id)["idUSER"]
    task_name = request.args.get('task_name', False)
    agree = request.args.get('agree', "")
    agree = bool(agree)
    comment=""

    print(user_id, user_index, task_name, agree, "asdas")

    if not (user_id and task_name and agree):
        flash("잘못된 승인절차입니다.")
        return redirect(f"/admin/tasks/{task_name}")
    
    if agree:
        new_status = "ongoing"
        services.admin.update_participation_status(task_name, user_index, new_status, comment)
        flash("승인 되었습니다.")
        return redirect(f"/admin/tasks/{task_name}")
    else:
        new_status = "reject"
        services.admin.update_participation_status(task_name, user_index, new_status, comment)
        flash("거절 되었습니다.")
        return redirect(f"/admin/tasks/{task_name}")


@controller.route("/tasks", methods=["POST"])
def add_task():
    '''태스크 추가 엔드포인트'''
    js = request.get_json()
    print(js)

    # js는 이렇게 생겼음
    # {'taskName': '', 'description': '', 'minPeriod': '', 'tableName': '', 'defaultFields': ['defaultField1', 'defaultField2'], 'originDataTypes': {'dataType1': { 'subField1': 'defaultField1', 'subField2': 'defaultField2'}, 'dataType2': {'subField3': 'defaultField1', 'subField4': 'defaultField2'}}, 'maxTupleRatio': 0, 'maxNullRatioPerColumn': 0, 'criteriaDescription': ''}

#     {
#   "taskName": "태스크 이름",
#   "description": "설명설명",
#   "minPeriod": "",
#   "tableName": "",
#   "defaultFields": [
#     "컬럼1",
#     "컬럼2",
#     "컬럼3"
#   ],
#   "originDataTypes": {
#     "원데타1": {
#       "컬컬럼럼1": "컬럼1",
#       "컬컬럼럼2": "컬럼2",
#       "컬컬럼럼3": "컬럼3"
#     },
#     "원데타2": {
#       "유유승승수수": "컬럼1",
#       "이이학학림림": "컬럼2",
#       "정정규규식식": "컬럼3"
#     }
#   },
#   "maxTupleRatio": "10",
#   "maxNullRatioPerColumn": "20",
#   "criteriaDescription": "이렇게 이렇게 이렇게 해주세용"
# }

#     task_name = js["taskName"]
#     task_name = js["task_name"]



    
    # TODO add task
    return "incomplete"


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
    user = services.users.get_user_by_index(estimator_index)
    tasks = services.estimator.evaluated_list(estimator_index)
    # participations = services.submitter.participating_tasklist(submitter_index)
    if not user:
        flash("해당 id에 대한 유저가 존재하지 않습니다")
        return redirect("/admin/")
    return render_template("admin/estimator.html",user=user,tasks=tasks)
# Create Read Update Delete(CRUD)
