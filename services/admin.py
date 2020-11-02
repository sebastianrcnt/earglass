from database.connection import connect


def getTasks(page):
    # 페이지 번호에 따른 task 리턴
    pass


def getUsers(page):
    # 페이지 번호에 따른 user 리턴
    pass


def searchUser(column, search_word, page):
    # column에 word로 검색한 결과를 page에 따라 리턴
    pass


def showSubmitter(user_id):
    # Submitter 에 대한 상세 정보 열람
    pass


def showEstimator(user_id):
    # Estimator에 대한 상세 정보 열람
    pass


def addTask(data):
    # 테스크 생성
    pass


def removeTask(task_id):
    # 테스크 제거
    pass


def editTask(task_id, data):
    # 테스크 수정
    pass


def showEstimateStatus(user_id):
    # 평가자 평가파일 현황
    pass


def showSubmitStatus(user_id):
    # 제출자 제출 현황
    pass
