from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib
import random
import codecs
from datetime import datetime

client = MongoClient('mongodb+srv://test:sparta@cluster0.zxyme.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.recycleKing

RANDOM_CHAR = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZ'
CHOISE_CHAR = ''

app = Flask(__name__)

SECRET_KEY = 'recycleKing'

def isLogin():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})
        return user_info
    except:
        return False

@app.route('/token')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})
        return render_template('fake_recycle.html', id=user_info['id'])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


######################################### 페이지 이동 주소 #############################################################

@app.route('/')
def login():
    return render_template('index.html')


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/result')
def result():
    return render_template("result.html")

######################################### API #########################################################################

# 로그인
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급
@app.route('/api/login', methods=['POST'])
def api_login():
    id = request.form['id']
    pw = request.form['pw']

    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    doc = {
      'id': id,
      'pw': pw_hash
    }

    result = db.users.find_one(doc)
    print(result)

    # 발견시 JWT 토큰 만들고 발급
    if result is not None:
        payload = {
           'id': id,

        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '동호수/비밀번호가 일치하지 않습니다.'})


# 회원가입
@app.route('/api/sign_up', methods=['POST'])
def api_sign_up():
    id = request.form['id']
    pw = request.form['pw']
    score = 0

    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    if db.users.find_one({'id':id}):
        return jsonify({'result': 'fail', 'msg': '다른 사람 집입니다.'})

    doc = {
        'id': id,
        'pw': pw_hash,
        'score' : score
    }

    db.users.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '회원가입 성공'})


# 동&호수 중복 확인
@app.route('/api/check_id', methods=['POST'])
def api_check_id():
    id = request.form['id']

    if db.users.find_one({'id': id}):
        return jsonify({'result': 'fail', 'msg': '다른 사람 집입니다.'})
    else:
        return jsonify({'result': 'success', 'msg': '본인 집입니다.'})

# id와 score 보내는 부분 (테스트)


@app.route('/fake')
def gorecycle():
    return render_template("fake_recycle.html")

@app.route("/api/submit", methods=["POST"])
def submit_post():
    login_user = isLogin()
    score_recieve = int(request.form['score_give'])
    update_score = login_user['score']+score_recieve
    db.users.update_one(login_user, {'$set': {'score': update_score}})

    return jsonify({'msg': '등록 완료!'})


# id와 score 가져오는 부분
@app.route("/api/result", methods=["GET"])
def submit_get():
    ranking_list = list(db.users.find({}, {'_id': False}))
    return jsonify({'ranking':ranking_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)