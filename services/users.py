from database.connection import *

def get_user_by_index(user_index):
    '''유저 인덱스로 유저 가져오기'''
    return queryone("SELECT * FROM USER WHERE idUSER=%s", (user_index,))

def get_user_by_id(user_id):
    '''유저 아이디로 유저 가져오기'''
    return queryone("SELECT * FROM USER WHERE Id=%s", (user_id,))

def get_userID_by_index(user_index):
    '''유저 인덱스로 유저 가져오기'''
    return queryone("SELECT Id FROM USER WHERE idUSER=%s", (user_index,))


def verify_user(user_id, password):
    '''주어진 아이디와 비밀번호랑 일치하는 유저가 있는지의 여부 확인'''
    user = get_user_by_id(user_id)
    if not user:
        return False
    elif user["Password"] != password:
        return False
    return True

def sign_up(user_id, password, name, birth, phonenumber, gender, address, role):
    '''새로운 유저 생성'''
    return callproc('InsertNewUser', (user_id, password, name,
                                      birth, phonenumber, gender, address, role))

def withdrawal(user_id, password):
    '''회원 탈퇴'''
    return callproc('DeleteUser',(user_id, password,))

def modify_user_info(user_id, password, name, birth, phonenumber, address):
    '''회원 정보 수정'''
    return callproc('UpdateUserInfo',(user_id, password, name, birth, phonenumber, address,))