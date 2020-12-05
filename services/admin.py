from database.connection import *
import math
import csv
from pprint import pprint
import json
from . import estimator

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


def edit_task(TaskName, Description, MinPeriod, MaxDuplicatedRowRatio, MaxNullRatioPerColumn, PassCriteria):
    '''수정된 정보 update'''
    sql = 'UPDATE TASK SET Description = %s, MinPeriod = %s, MaxDuplicatedRowRatio = %s, MaxNullRatioPerColumn = %s, PassCriteria = %s WHERE TaskName = %s;'

    print((Description, MinPeriod, MaxDuplicatedRowRatio, MaxNullRatioPerColumn, PassCriteria, TaskName))
    execute(sql, (Description, MinPeriod, MaxDuplicatedRowRatio, MaxNullRatioPerColumn, PassCriteria, TaskName))

def task_info(task_name):
    '''태스크 정보 반환'''
    sql = "SELECT * FROM TASK WHERE TaskName = %s"
    return queryone(sql, (task_name, ))

def task_info_origin_data_type(task_name):
    '''태스크 정보에서 원본 데이터 타입 별로 제출 파일 수, Pass된 파일 수 보여주기'''
    sql = "SELECT ODT.*, COUNT(P.idPARSING_DSF) AS SubmitNum, \
            SUM(CASE COALESCE(P.Pass, 'NP') WHEN 'P' THEN 1 ELSE 0 END) AS PassNum \
            FROM ORIGIN_DATA_TYPE AS ODT LEFT OUTER JOIN PARSING_DSF AS P ON P.OriginDataTypeID = ODT.idORIGIN_DATA_TYPE \
            WHERE ODT.TaskName = %s \
            GROUP BY ODT.DataTypeName"
    return queryall(sql, (task_name, ))

def stop_task(task_name):
    '''task 강제 종료'''
    return callproc('StopTask', (task_name,))

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
    return queryone(sql, (task_name, status, ))

def count_total_task_pdsf(task_name):
    '''전체 pdsf 파일 수'''
    sql = "SELECT COUNT(*) AS count FROM PARSING_DSF WHERE TaskName = %s"
    return queryall(sql, (task_name, ))


def add_task(task_name, description, min_period, task_data_table_name,
         max_duplicated_row_ratio, max_null_ratio_per_column, pass_criteria, schema_info):
    '''태스크 추가'''
    return callproc('InsertNewTask', (task_name, description, int(min_period), task_data_table_name,
         float(max_duplicated_row_ratio), float(max_null_ratio_per_column), pass_criteria, schema_info,))


def get_all_tasks():
    '''taskname, task 통계(제출 파일 수, pass된 파일 수), task data table 위치'''
    sql = "SELECT TASK.*, \
        (SELECT COUNT(TaskName) FROM PARSING_DSF WHERE PARSING_DSF.TaskName=TASK.TaskName) as ParsingDsfCount, \
        (SELECT COUNT(TaskName) FROM PARSING_DSF WHERE PARSING_DSF.Pass='P' AND PARSING_DSF.TaskName=TASK.TaskName) as PassedParsingDsfCount \
        FROM TASK"
    return queryall(sql)


def add_origin_data_type(task_name, data_type_name, schema_info, mapping_info):
    '''해당 task의 원본 데이터 타입 정보 추가'''
    return callproc('InsertOriginDataType', (task_name, data_type_name, schema_info, mapping_info))