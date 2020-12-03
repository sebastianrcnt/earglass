from database.connection import *


def evaluate_waiting_list(estimator_index):#ROW_NUMBER 지움
    """해당 평가자가 평가할 파일 리스트 (index, taskname, 제출자 id, deadline, 파싱dsf 위치)"""
    sql = "SELECT P.TaskName, P.SubmitterID, E.Deadline, P.ParsingFile, P.idPARSING_DSF\
    FROM EVALUATION AS E, PARSING_DSF AS P\
    WHERE P.idPARSING_DSF = E.FK_idPARSING_DSF AND E.FK_idEstimator = %s AND E.Status = 'ongoing'"
    return queryall(sql, (estimator_index, ))

def evaluated_list(estimator_index): #ROW_NUMBER 지움
    """해당 평가자가 평가한 파일 리스트 (index, taskname, 제출자 id, 평가점수, pass여부, 평가한날짜와시간, 파싱dsf 위치)"""
    sql = "SELECT P.TaskName, P.SubmitterID, E.Score, E.Pass, E.EndTime, P.ParsingFile\
    FROM EVALUATION AS E, PARSING_DSF AS P LEFT JOIN TASK AS T ON P.TaskName = T.TaskName \
    WHERE P.idPARSING_DSF = E.FK_idPARSING_DSF AND E.FK_idEstimator = %s AND E.Status = 'done'"
    return queryall(sql, (estimator_index, ))

def task_detail(task_name):
    """태스크 이름으로 태스크 상세 가져오기"""
    sql = "SELECT * FROM TASK WHERE TaskName = %s"
    return queryone(sql, (task_name, ))

def odsf_mapping_info(task_name):
    '''해당 태스크의 원본 데이터 타입 스키마 매핑 정보를 가져와서 태스크 상세 페이지에 보여주기'''
    sql = "SELECT DataTypeName, MappingInfo FROM ORIGIN_DATA_TYPE WHERE TaskName = %s"
    return queryall(sql, (task_name, ))

    
def is_done(estimator_index, parsing_dsf_id):
    """해당 평가자에 대하여, 해당 파싱 파일이 평가완료되었는지 여부 반환 (ongoing, done)"""
    sql = "SELECT Status FROM EVALUATION WHERE FK_idEstimator = $s AND FK_idPARSING_DSF = $s"
    return queryone(sql, (int(estimator_index), int(parsing_dsf_id), ))

def pdsf_file_info(parsing_dsf_id):
    '''parsing_dsf_id를 주면 해당 row의 typename과 parsingfile 반환'''
    sql = "SELECT TaskName, ParsingFile, TotalStatus, Pass, FK_idORIGIN_DSF FROM PARSING_DSF WHERE idPARSING_DSF = %s"
    return queryone(sql, (int(parsing_dsf_id,)))

def update_evaluation_status(parsing_dsf_id, estimator_index, score, is_passed):
    """평가를 끝냈을 때 db 업데이트"""
    return callproc('UpdateEvaluationStatus', (parsing_dsf_id, estimator_index, score, is_passed))

# def update_system_score(parsing_dsf_id, system_score):
#     '''파일이 제출되었을 때, system score 받아와서 DB 업데이트'''
#     return callproc('UpdateSystemScore', (parsing_dsf_id, system_score))
