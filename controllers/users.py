import re
from flask import Blueprint, render_template, redirect, request, make_response, flash
import services

controller = Blueprint("users", __name__)

# Pages
@controller.route("/", methods=['GET'])
def get_user():
    # 쿠키가 있다 -> 로그인된 유저라면
    user_id = request.cookies.get("user_id")
    user = services.users.get_user_by_id(user_id)

    if user:  # 로그인 된 경우
        if user['FK_UserTypeName'] == "관리자" :
            return render_template("auth/admin_my.html", user=user)
        else :
            return render_template("auth/my.html", user=user)
    else:
        flash("로그인되지 않았습니다")
        return redirect("/")

# template가 불안정
@controller.route("/edit", methods=['POST'])
def edit_user():
    user_id = request.cookies.get("user_id")
    user = services.users.get_user_by_id(user_id)
    data = request.form

    # check validation by
    valid_password = re.fullmatch("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", data["password"])
    valid_birth = re.fullmatch('\d{8}', data["birth"])
    valid_phonenumber = re.fullmatch('^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$', data["phonenumber"])

    if not (valid_password):
        flash("비밀번호는 8~24자 영문대소문자, 숫자, 특수문자 혼합 사용해야합니다.")
        return render_template("back.html")

    if not (valid_birth):
        flash("생년월일 형식이 알맞지 않습니다. YYYYMMDD")
        return render_template("back.html")

    if not (valid_phonenumber):
        flash("전화번호 형식이 알맞지 않습니다. XXX-XXXX-XXXX")
        return render_template("back.html")

    return redirect("/users/")


# Auth Stuff
@controller.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("username")
    password = request.form.get("password")

    response = make_response(redirect("/"))
    # login 성공 여부 확인
    if services.users.verify_user(user_id, password):
        user = services.users.get_user_by_id(user_id)
        response.set_cookie("user_id", user_id)
        response.set_cookie("user_index", str(user["idUSER"]))
        return response
    else:
        flash("로그인 실패. 다시 시도하세요")
    return response


@controller.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie("user_id")
    return response

@controller.route("/signup", methods=["GET"])
def get_signup_page():
    return render_template("auth/sign_up.html")


@controller.route("/signup", methods=["POST"])
def sign_up():
    data = request.form

    # check validation by
    valid_password = re.fullmatch("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", data["password"])
    valid_birth = re.fullmatch('\d{8}', data["birth"])
    valid_phonenumber = re.fullmatch('^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$', data["phonenumber"])

    if not (valid_password):
        flash("비밀번호는 8~24자 영문대소문자, 숫자, 특수문자 혼합 사용해야합니다.")
        return render_template("back.html")

    if not (valid_birth):
        flash("생년월일 형식이 알맞지 않습니다. YYYYMMDD")
        return render_template("back.html")

    if not (valid_phonenumber):
        flash("전화번호 형식이 알맞지 않습니다. XXX-XXXX-XXXX")
        return render_template("back.html")

    # try sign up
    log = services.users.sign_up(data["id"], data["password"], data["name"], data["birth"], data["phonenumber"], data["gender"], data["address"], data["role"])
    log = log[0].popitem()

    if log[0] == 'InsertNewUserErrorMessage' and log[1] == 'User ID already exists.':
        flash("이미 존재하는 아이디입니다.")
        return render_template("back.html")

    flash("회원가입이 완료되었습니다.")
    return redirect("/")

@controller.route("/my/edit", methods=["GET"])
def edit():
    user_id = request.cookies.get("user_id")
    user = services.users.get_user_by_id(user_id)
    return render_template("auth/modify_my.html",user=user)

@controller.route("/admin_edit", methods=["GET"])
def get_admin_edit_page():
    user_id = request.cookies.get("user_id")
    user = services.users.get_user_by_id(user_id)
    return render_template("auth/modify_admin.html",user=user)

@controller.route("/admin_edit", methods=["POST"])
def admin_edit():
    user_id = request.cookies.get("user_id")
    user = services.users.get_user_by_id(user_id)

    get_data = request.form
    password = get_data['password']
    name = user['Name']
    birth = user['BirthDate']
    phonenumber = user['PhoneNum']
    address = user['Address']

    try :
        log = services.users.modify_user_info(user_id, password, name, birth, phonenumber, address)
    except:
        pass

    return redirect("/users/")
    
@controller.route("/my/withdrawal", methods=["GET"])
def get_withdrawal_page():
    user_id = request.cookies.get("user_id")
    user = services.users.get_user_by_id(user_id)
    user_pw = user['Password']

    return render_template("auth/withdrawal.html", user=user)

@controller.route("/withdrawal", methods=["POST"])
def withdrawal():
    user_id = request.cookies.get("user_id")
    user = services.users.get_user_by_id(user_id)
    user_pw = user['Password']
    password = request.form.get("password")
    if user_pw==password:
        log = services.users.withdrawal(user_id, user_pw)
        flash("성공적으로 탈퇴되었습니다")
        return redirect("/")
    else:
        flash("비밀번호가 틀렸습니다")
    return render_template("/auth/withdrawal.html",user=user)