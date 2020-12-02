from flask import Blueprint, render_template, redirect, request, make_response, flash
import services

controller = Blueprint("task", __name__)

@controller.route("/detail", methods=["GET"])
def task_detail():
    user_index = int(request.cookies.get("user_index"))
    task_name = request.args.get('task_name', 0)
    tab = request.args.get('tab', 'info')

    # db 테스크 정보를 주세요
    task_info = services.submitter.task_info(task_name)

    leaderboard = services.submitter.leaderboard(task_name)

    total_my_submission = services.submitter.my_submission_list(task_name, user_index)
    for pdsf in total_my_submission:
        pdsf["ParsingFile"] = pdsf["ParsingFile"].split("/")[-1]

    odsf_type = services.submitter.all_origin_data_type(task_name)
    
    data_type_table_dict={}
    for i in odsf_type:
        data_type_table_dict[i["idORIGIN_DATA_TYPE"]] = services.submitter.sort_by_origin_data_type(task_name,user_index,i["idORIGIN_DATA_TYPE"])
        for pdsf in data_type_table_dict[i["idORIGIN_DATA_TYPE"]]:
            pdsf["ParsingFile"] = pdsf["ParsingFile"].split("/")[-1]

    return render_template("task/task_detail.html", opt=tab, task_info=task_info, leaderboard=leaderboard, total_my_submission=total_my_submission, odsf_type=odsf_type,data_type_table_dict=data_type_table_dict)
