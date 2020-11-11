import re
from flask import Blueprint, render_template, redirect, request, make_response, flash
from services import users

controller = Blueprint("users", __name__)


@controller.route("/login", methods=["POST"])
def post_login_data():
    user_id = request.form.get("username")
    password = request.form.get("password")

    response = make_response(redirect("/"))
    # login 성공 여부 확인
    if users.verify_user(user_id, password):
        # not "/my", "my". "my" == "/users/my", "/my" = "/my"
        response.set_cookie("user_id", user_id)
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
def sign_up_form():
    return render_template("auth/sign_up.html")


@controller.route("/signup", methods=["POST"])
def sign_up():
    print(request.form)
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

    # 디비가 구축되고 나면 해야함!!!!
    # [{'InsertNewUserErrorMessage': 'User ID already exists.'}]
    # [{'InsertNewUserSuccessMessage': 'Insert new User successfully'}]
    try:
        # try sign up
        log = users.sign_up(data["id"], data["password"], data["name"], data["birth"], data["phonenumber"], data["gender"], data["address"], data["role"])
        print(log)
        log_type = log[0].keys()[0]
        log_value = log[0].items()[0]
        print(log_type, log_value)
    except:
        pass

    return redirect("/")


@controller.route("/my", methods=['GET'])
def mypage():
    # 쿠키가 있다 -> 로그인된 유저라면
    user_id = request.cookies.get("user_id")
    print('user_id:', user_id)
    user = users.get_user_by_id(user_id)

    if user:  # 로그인 된 경우
        return render_template("auth/my.html", user=user)
    else:
        flash("로그인되지 않았습니다")
        return redirect("/")

# template가 불안정
@controller.route("/my/edit", methods=['GET'])
def edit_my_form():
    return render_template("auth/modify_my.html")



# made by 학림, 함수명은 목적 페이지로!
@controller.route("/tests", methods=["GET"])
def tests():
    return render_template("submitter/submitter_home.html")
