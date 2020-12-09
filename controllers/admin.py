# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request, make_response, flash, send_file, Response
import services
import system
import pandas as pd
from io import StringIO
import json
from database.connection import queryall, queryone

# writed by seungsu

controller = Blueprint("admin", __name__)

# /


@controller.route("/", methods=["GET"])
def get_admin_page():
    tasks = services.admin.get_all_tasks()
    for task in tasks:
        task["total_passed_row"] = system.utils.count_row_by_origin_type(task['TaskName'], [])['total']


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

    if len(submitters) == 0:
        users = estimators
    elif len(estimators) == 0:
        users = submitters
    else:
        users = submitters + estimators
    return render_template("admin/index.html", users=users, tasks=tasks)

@controller.route("/add_task", methods=["GET"])
def get_add_task_page():
    '''태스크 추가 페이지'''
    return render_template("admin/add_task.html")


@controller.route("/tasks/<task_name>", methods=["GET"])
def get_task_page(task_name):
    '''태스크 상세페이지'''
    task = services.admin.task_info(task_name)
    origin_data_types = services.admin.task_info_origin_data_type(task_name)
    task_participation = services.admin.show_task_participation_list(task_name)

    task['TaskDataTableName'] = task['TaskDataTableName'].split("/")[-1]
    # task['SchemaInfo'] = json.loads(task['SchemaInfo'])

    odt_list = []
    for odt in origin_data_types:
        odt_list.append(odt['idORIGIN_DATA_TYPE'])
    count_row_by_odt = system.utils.count_row_by_origin_type(task_name, odt_list)
    total_file_num = services.admin.count_total_task_pdsf(task_name)[0]["count"]

    for odt in origin_data_types:
        odt['MappingInfo'] = json.loads(odt['MappingInfo'])
    return render_template("admin/task_info.html", task_name=task_name,task=task, origin_data_types=origin_data_types, task_participation=task_participation, count_row_by_odt=count_row_by_odt, total_file_num= total_file_num)

@controller.route("/tasks-ajax/add-odt/<task_name>", methods=["POST"])
def add_odsf(task_name):
    js = request.get_json()
    data_type_name = js.get('name')
    schema_info = ','.join(js.get('defaultFields'))
    mapping_info = json.dumps(js.get('subFields'))
    services.admin.add_origin_data_type(task_name, data_type_name, schema_info, mapping_info)
    return "Successfully Added", 201

@controller.route("/tasks-ajax/stop/<task_name>", methods=["GET"])
def stop_task(task_name):
    services.admin.stop_task(task_name)
    return "Successfully Stopped", 200

@controller.route("/tasks/agreement", methods=["GET"])
def confirm_agreement():
    """
    태스크 참여 신청 처리
    """
    # TODO 관리자인지 확인 필요

    user_id = request.args.get('user_id', False)
    user_index = services.users.get_user_by_id(user_id)["idUSER"]
    task_name = request.args.get('task_name', False)
    agree = request.args.get('agree', "")
    comment=""
    
    if not (user_id and task_name and agree):
        flash("잘못된 승인절차입니다.")
        return redirect(f"/admin/tasks/{task_name}")
    
    if agree == 'True':
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
def task_add():
    '''태스크 추가 엔드포인트'''
    js = request.get_json()

    task_name = js["taskName"]
    description = js["description"]
    min_period = js["minPeriod"]
    defaultFields = ",".join(js["defaultFields"])
    originDataTypes = js["originDataTypes"]
    max_duplicated_row_ratio = float(js["maxTupleRatio"])
    max_null_ratio_per_column = float(js["maxNullRatioPerColumn"])
    pass_criteria = js["criteriaDescription"]

    task_data_table_name = f"{task_name}_data_table.csv"

    # save task data table
    js["defaultFields"].append("submitter_name")
    js["defaultFields"].append("origin_type")
    task_data_df = pd.DataFrame(columns=js["defaultFields"])
    task_data_table_name = system.utils.save_df("table_data", task_data_table_name, task_data_df)

    services.admin.add_task(task_name, description, min_period, task_data_table_name, max_duplicated_row_ratio, max_null_ratio_per_column, pass_criteria, defaultFields)

    for data_type_name, columns in originDataTypes.items():
        schema_info = list(columns.keys())
        schema_info = ",".join(schema_info)
        mapping_info = json.dumps(columns, ensure_ascii=False)

        services.admin.add_origin_data_type(task_name, data_type_name, schema_info, mapping_info)
    redirect_url = f"/admin/tasks/{task_name}"
    return redirect(redirect_url)
    # return render_template("admin/add_task.html")

@controller.route("/tasks/<task_name>", methods=["POST"])
def edit_task(task_name):
    '''태스크 수정 엔드포인트'''
    # TODO edit task
    TaskName = task_name
    Description = request.form.get('Description')
    MinPeriod = request.form.get('MinPeriod')
    MinPeriod = float(MinPeriod)
    MaxDuplicatedRowRatio = request.form.get('MaxDuplicatedRowRatio')
    MaxDuplicatedRowRatio = float(MaxDuplicatedRowRatio)
    MaxNullRatioPerColumn = request.form.get('MaxNullRatioPerColumn')
    MaxNullRatioPerColumn = float(MaxNullRatioPerColumn)
    PassCriteria = request.form.get("PassCriteria")

    services.admin.edit_task(TaskName, Description, MinPeriod, MaxDuplicatedRowRatio, MaxNullRatioPerColumn, PassCriteria)

    redirect_url = f"/admin/tasks/{task_name}"

    return redirect(redirect_url)

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
    
    # preprocessing
    for task in tasks:
        task["ParsingFile"] = task["ParsingFile"].split("/")[-1]

    return render_template("admin/estimator.html",user=user,tasks=tasks)
# Create Read Update Delete(CRUD)

@controller.route("/task/download/<task_name>")
def csv_file_download_with_stream(task_name):
    """
    pdsf csv file download
    """
    
    filename = services.admin.task_info(task_name)["TaskDataTableName"]
    fname = filename.split("/")[-1]
    temp_df = pd.read_csv(filename, encoding='utf-8')

    # 그 결과를 앞서 만든 IO stream에 저장
    output_stream = StringIO()

    temp_df.to_csv(output_stream, index=False, encoding='utf-8')
    response = Response(
        output_stream.getvalue(),
        mimetype='text/csv; charset=utf-8',
        content_type='application/octet-stream',
    )

    response.headers["Content-Disposition"] = f"attachment; filename={fname}".encode('utf-8')

    return response
