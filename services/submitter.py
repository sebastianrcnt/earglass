from database.connection import *


def tasklist_detail(user_index):
    """진행 중인 태스크에 taskname,
    참여상태(진행중, 대기중, 거절됨.. 이거는 버튼에 반영) 보여주기""" 
    sql = "SELECT T.TaskName, COALESCE(P.Status, '') AS Status \
    FROM TASK AS T LEFT OUTER JOIN PARTICIPATION AS P ON P.FK_TaskName = T.TaskName AND P.FK_idUSER = %s WHERE T.Status = 'ongoing'"
    return queryall(sql, (user_index,))

def participating_tasklist(user_index):
    """참여자가 참여중인 태스크 정보 taskname, submit_num, pass 수"""
    sql = "SELECT SQ.TaskName, SQ.Status, MAX(COALESCE(D.SubmitNum, 0)) AS Submit_num, \
    SUM(CASE COALESCE(D.Pass, 'NP') WHEN 'P' THEN 1 ELSE 0 END) AS Pass_num \
    FROM (SELECT T.TaskName, COALESCE(P.Status, '') AS Status\
        FROM TASK AS T LEFT OUTER JOIN PARTICIPATION AS P ON P.FK_TaskName = T.TaskName AND P.FK_idUSER = %s) AS SQ\
    LEFT OUTER JOIN PARSING_DSF AS D ON D.TaskName = SQ.TaskName \
    WHERE SQ.Status = 'ongoing' GROUP BY SQ.TaskName"
    return queryall(sql, (user_index,))

def task_info(task_name):
    """태스크 정보"""
    sql = "SELECT * FROM TASK WHERE TaskName = %s"
    return queryone(sql, (task_name, ))

def leaderboard(task_name):
    """특정 태스크의 전체 참여자의 제출 현황
    제출자 id, 원본 데이터 타입, 평가점수, pass여부
    점수 순으로 sorting"""
    sql = "SELECT P.SubmitterID, O.DataTypeName, P.TotalScore, P.Pass \
    FROM PARSING_DSF AS P LEFT JOIN ORIGIN_DATA_TYPE AS O ON P.OriginDataTypeID = O.idORIGIN_DATA_TYPE \
    WHERE P.TaskName = %s ORDER BY P.TotalScore DESC"
    return queryall(sql, (task_name, ))

def my_submission_list(task_name, user_index):
    """회차, 기간, 제출파일명, 원본데이터타입, 날짜, 시스템점수, 평가자점수(평균), total 점수, pass여부"""
    sql = "SELECT P.Round, P.Period, P.ParsingFile, ODT.DataTypeName, O.DateTime, P.SystemScore, P.AverageScore, P.TotalScore, P.Pass \
    FROM PARSING_DSF AS P, ORIGIN_DSF AS O LEFT JOIN ORIGIN_DATA_TYPE AS ODT ON O.FK_idORIGIN_DATA_TYPE = ODT.idORIGIN_DATA_TYPE \
    WHERE P.FK_idORIGIN_DSF = O.idORIGIN_DSF and P.TaskName = %s and P.SubmitterID = %s"
    return queryall(sql, (task_name, user_index, ))

def submit_info(task_name):
    """taskname, 스키마 정보, 매핑 정보"""
    sql = "SELECT SchemaInfo, MappingInfo FROM ORIGIN_DATA_TYPE WHERE TaskName = %s"
    return queryall(sql, (task_name, ))

def odsf_type_schema_info(odsf_type_id):
    """taskname, 스키마 정보, 매핑 정보"""
    sql = "SELECT * FROM ORIGIN_DATA_TYPE WHERE idORIGIN_DATA_TYPE = %s"
    return queryone(sql, (odsf_type_id, ))

def submit_pdsf(task_name, parsing_file, origin_data_type_id, submitter_id, period, round, origin_dsf_id, system_score):
    '''시스템을 거쳐서 orgin_dsf를 parsing_dsf로 변환하여 저장'''
    return callproc('InsertParsingDSF', (task_name, parsing_file, origin_data_type_id, submitter_id, period, round, origin_dsf_id, system_score))

def submit_odsf(origin_file, datetime, period, task_name, user_index, origin_data_type_id, round):
    """제출자 파일을 받으면 origin_dsf로 저장"""
    return callproc('InsertOriginDSF', (origin_file, datetime, period, task_name, user_index, origin_data_type_id, round ))

def search_odsf_by_filepath(odsf_file):
    sql = "SELECT * FROM ORIGIN_DSF WHERE OriginFile = %s"
    return queryone(sql, (odsf_file, ))

def insert_participation(task_name, user_index):
    """참여 요청"""
    return callproc('InsertNewParticipation', (task_name, user_index,))

def sort_by_origin_data_type(task_name, user_index, origin_data_type_id):
    """원본 데이터 타입에 따라 내 제출 현황 보여주기"""
    sql = "SELECT P.Round, P.Period, P.ParsingFile, ODT.DataTypeName, O.DateTime, P.SystemScore, P.AverageScore, P.TotalScore, P.Pass \
    FROM PARSING_DSF AS P, ORIGIN_DSF AS O LEFT JOIN ORIGIN_DATA_TYPE AS ODT ON O.FK_idORIGIN_DATA_TYPE = ODT.idORIGIN_DATA_TYPE \
    WHERE P.FK_idORIGIN_DSF = O.idORIGIN_DSF and P.TaskName = %s and P.SubmitterID = %s and P.OriginDataTypeID = %s ORDER BY P.Round"
    return queryall(sql, (task_name, user_index, origin_data_type_id, ))

def sort_by_pass(task_name, user_index,p_np):
    """pass 여부에 따라 내 제출 현황 보여주기"""
    sql = "SELECT P.Round, P.Period, P.ParsingFile, ODT.DataTypeName, O.DateTime, P.SystemScore, P.AverageScore, P.TotalScore, P.Pass \
    FROM PARSING_DSF AS P, ORIGIN_DSF AS O LEFT JOIN ORIGIN_DATA_TYPE AS ODT ON O.FK_idORIGIN_DATA_TYPE = ODT.idORIGIN_DATA_TYPE \
    WHERE P.FK_idORIGIN_DSF = O.idORIGIN_DSF and P.TaskName = %s and P.SubmitterID = %s and P.Pass = %s"
    return queryall(sql, (task_name, user_index, p_np, ))

def all_origin_data_type(task_name):
    """해당 task의 모든 원본 데이터 타입 리스트 반환"""
    sql = "SELECT * FROM ORIGIN_DATA_TYPE WHERE TaskName = %s"
    return queryall(sql, (task_name, ))
