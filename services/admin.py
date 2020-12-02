from database.connection import *
import math
import csv
from pprint import pprint
import json
from . import estimator

# CRUD

# GET
def get_waiting_dsf_by_estimator_index(estimator_index):
    '''평가자 평가할 파싱 파일 현황'''
    return estimator.evaluate_waiting_list(estimator_index)

def get_completed_dsf_by_estimator_index(estimator_index):
    '''평가자 평가한 파싱 파일 현황'''
    return estimator.evaluated_list(estimator_index)

def get_participating_tasks_by_user_index(user_index):
    '''해당 유저가 참여 중인 태스크 목록'''
    sql = "SELECT SQ.TaskName, MAX(COALESCE(D.SubmitNum, 0)) AS SubmitNum, \
    SUM(CASE COALESCE(D.Pass, 'NP') WHEN 'P' THEN 1 ELSE 0 END) AS PassNum \
    FROM (SELECT T.TaskName, COALESCE(P.Status, '') AS Status\
        FROM TASK AS T LEFT OUTER JOIN PARTICIPATION AS P ON P.FK_TaskName = T.TaskName AND P.FK_idUSER = %s) AS SQ\
    LEFT OUTER JOIN PARSING_DSF AS D ON D.TaskName = SQ.TaskName \
    WHERE SQ.Status = 'ongoing' GROUP BY SQ.TaskName"
    return queryall(sql, (user_index, ))

def get_origin_data_types(user_index, task_name):
    '''원본 데이터 타입 별로 보여주기
    제출 파일 수, pass된 파일 수'''
    sql = "SELECT O.DataTypeName,  MAX(COALESCE(P.SubmitNum, 0)) AS SubmitNum, \
        SUM(CASE COALESCE(P.Pass, 'NP') WHEN 'P' THEN 1 ELSE 0 END) AS PassNum \
        FROM PARSING_DSF AS P, ORIGIN_DATA_TYPE AS O WHERE P.OriginDataTypeID = O.idORIGIN_DATA_TYPE \
             AND P.SubmitterID = %s AND P.TaskName = %s"
    return queryall(sql, (user_index, task_name, ))

# UPDATE
def update_participation_status(task_name, user_index, new_status, comment):
    '''제출자의 참여 상태 업데이트'''
    return callproc('UpdateParticipationStatus', (task_name, user_index, new_status, comment,))


def edit_task(current_task_name, description, min_period, status, task_data_table_name,
         max_duplicated_row_ratio, max_null_ratio_per_column, pass_criteria):
    '''수정된 정보 update'''
    return callproc('EditTask', (current_task_name, description, min_period, status, task_data_table_name,
         max_duplicated_row_ratio, max_null_ratio_per_column, pass_criteria,))

def task_info(task_name):
    '''태스크 정보 반환'''
    sql = "SELECT TaskName, Description, MinPeriod, TaskDataTableName, TaskDataTableSchemaInfo, MaxDuplicatedRowRatio, MaxNullRatioPerColumn \
        FROM TASK WHERE TaskName = %s"
    return queryone(sql, (task_name, ))

def task_info_origin_data_type(task_name):
    '''태스크 정보에서 원본 데이터 타입 별로 제출 파일 수, Pass된 파일 수 보여주기'''
    sql = "SELECT ODT.DataTypeName, COUNT(P.idPARSING_DSF) AS SubmitNum, \
            SUM(CASE COALESCE(P.Pass, 'NP') WHEN 'P' THEN 1 ELSE 0 END) AS PassNum \
            FROM ORIGIN_DATA_TYPE AS ODT LEFT OUTER JOIN PARSING_DSF AS P ON P.OriginDataTypeID = ODT.idORIGIN_DATA_TYPE \
            WHERE ODT.TaskName = %s \
            GROUP BY ODT.DataTypeName"
    return queryall(sql, (task_name, ))

def stop_task(task_name):
    '''task 강제 종료'''
    return callproc('StopTask', (task_name,))

def delete_task(task_name):
    '''task delete'''
    return callproc('DeleteTask', (task_name,))

def show_task_participation_list(task_name):
    '''index, 참여자 id, 제출자 평가 점수'''
    sql = "SELECT P.Status, U.Id, U.UserScore \
        FROM PARTICIPATION AS P, USER AS U \
        WHERE P.FK_idUSER = U.idUSER AND P.FK_TaskName = %s"
    return queryall(sql, (task_name, ))

def sort_task_participation_list(task_name, status):
    '''참여 상태별로 sorting'''
    sql = "SELECT All_Status.Status, All_Status.Id, All_Status.UserScore \
        FROM (SELECT P.Status, U.Id, U.UserScore \
        FROM PARTICIPATION AS P, USER AS U \
        WHERE P.FK_idUSER = U.idUSER AND P.FK_TaskName = %s) AS All_Status \
        WHERE All_Status.Status = %s"
    return queryall(sql, (task_name, status, ))


def add_task(task_name, description, min_period, status, task_data_table_name,
         max_duplicated_row_ratio, max_null_ratio_per_column, pass_criteria, schema_info):
    '''태스크 추가'''
    return callproc('InsertNewTask', (task_name, description, min_period, status, task_data_table_name,
         max_duplicated_row_ratio, max_null_ratio_per_column, pass_criteria, schema_info,))


def get_all_tasks():
    '''taskname, task 통계(제출 파일 수, pass된 파일 수), task data table 위치'''
    sql = "SELECT TASK.*, \
        (SELECT COUNT(TaskName) FROM PARSING_DSF WHERE PARSING_DSF.TaskName=TASK.TaskName) as ParsingDsfCount, \
        (SELECT COUNT(TaskName) FROM PARSING_DSF WHERE PARSING_DSF.Pass='P' AND PARSING_DSF.TaskName=TASK.TaskName) as PassedParsingDsfCount \
        FROM TASK"
    return queryall(sql)

# def user_exists(user_id):
#     '''user_id가 존재하면 true, 존재하지 않으면 false'''
#     user = queryone("SELECT * FROM USER WHERE Id=%d", (user_id, ))
#     if user:
#         return True
#     return False

# # Exists
# def task_exists(task_name):
#     '''taskname이 존재하면 true, 존재하지 않으면 false'''
#     task = queryone("SELECT * FROM TASK WHERE TaskName=%s", (task_name, ))
#     if task:
#         return True
#     return False

# def data_type_name_exists(task_name, data_type_name):
#     '''data type name이 존재하면 true, 존재하지 않으면 false'''
#     assert task_exists(task_name)
#     found = queryone("SELECT * FROM ORIGIN_DATA_TYPE WHERE TaskName=%s AND DataTypeName=%s", (task_name, data_type_name))
#     if not found:
#         return False
#     return True

# # Doesn't Exists
# def get_default_fields_of_task(task_name):
#     '''해당 task의 고유 스키마 정보 반환'''
#     task = queryone("SELECT (TaskDataTableSchemaInfo) FROM TASK WHERE `TaskName`=%s", (task_name, ))
#     result = task['TaskDataTableSchemaInfo'].split(',')
#     return result

# def set_default_fields_of_task(task_name, default_fields):
#     '''해당 tastk의 고유 스키마 정보 수정(삽입)'''
#     assert task_exists(task_name)
#     default_fields = ",".join(default_fields)
#     execute("UPDATE TASK SET TaskDataTableSchemaInfo=%s WHERE TaskName=%s", (default_fields, task_name))

def add_origin_data_type(task_name, data_type_name, schema_info, mapping_info):
    '''해당 task의 원본 데이터 타입 정보 추가'''
    return callproc('InsertOriginDataType', (task_name, date_type_name, schema_info, mapping_info))

# def remove_origin_data_type(task_name, data_type_name):
#     '''해당 task name에서 특정 origin data type 삭제'''
#     assert task_exists(task_name)
#     execute("DELETE FROM ORIGIN_DATA_TYPE WHERE DataTypeName=%s AND TaskName=%s", (data_type_name, task_name))

# def get_mapping_info(task_name, data_type_name):
#     '''mapping info 리턴'''
#     assert task_exists(task_name)
#     assert data_type_name_exists(task_name, data_type_name)
#     original_data_type = queryone("SELECT (MappingInfo) FROM ORIGIN_DATA_TYPE")
#     mapping_info = original_data_type['MappingInfo']
#     return mapping_info

# def set_mapping_info(task_name, data_type_name, mapping_info):
#     '''mapping info 업데이트'''
#     assert task_exists(task_name)
#     assert data_type_name_exists(task_name, data_type_name)
#     used_default_fields = set(mapping_info.values())
#     allowed_default_fields = set(get_default_fields_of_task(task_name))
#     print(used_default_fields.issubset(allowed_default_fields))
#     if used_default_fields.issubset(allowed_default_fields):
#         execute("UPDATE ORIGIN_DATA_TYPE SET MappingInfo=%s WHERE DataTypeName=%s AND TaskName=%s", (json.dumps(mapping_info), data_type_name, task_name))

