import os

from flask import Flask
from flask import json
from flask import request
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from config import TONGUE


app = Flask(__name__)
# app.jinja_env.variable_start_string = '{{ '
# app.jinja_env.variable_end_string = ' }}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format("kos.db")
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


@app.route('/')
def hello_world():
    print(root)
    return send_from_directory(root, "index.html")


@app.route('/<username>/items', methods=['GET', 'POST'])
def new_user(username):
    from s_database import Sentence, User

    if request.method == 'GET':
        user_id = User.query.filter_by(user_name=username).first().user_id
        all_sentence = Sentence.query.filter_by(user_id=user_id).all()

        # if isinstance(all_sentence, list):
        #     return [json.dumps(item) for item in all_sentence]
        # else:i
        #     return json.dumps(all_sentence)
        if not isinstance(all_sentence, list):
            all_sentence = [all_sentence]

        return jsonify(user_id=user_id, sentences=
            [
                {
                    "sentence_id": item.sentence_id,
                    "chinese": item.chinese,
                    "english": item.english,
                    "type": item.type,
                }
                for item in all_sentence
                ]
        )
    elif request.method == "POST":
        from datetime import datetime
        if 'chinese' in request.form and 'english' in request.form \
                and 'user_id' in request.form and 'create_time' in request.form:
            new_sentence = Sentence(request.form['english'], request.form['user_id'],
                                    datetime.utcnow(), request.form['chinese'],
                                    TONGUE)
            db.session.add(new_sentence)
            db.session.commit()
            return_message = {"code": True, "message": "Add success!", "sentence_id": new_sentence.sentence_id}
        else:
            return_message = {"code": False, "message": "argument is wrong!", "sentence_id": -1}

        return jsonify(return_message)
    else:
        return "ERROR!!!"


@app.route('/<username>/items/<sentence_id>', methods=['DELETE'])
def delete_sentence(username, sentence_id):
    from s_database import Sentence
    need_del_sentence = Sentence.query.filter_by(sentence_id=sentence_id).first()
    # need_del_sentence需要转换成对象，这里delete才能成功，因为delete这里需要的是一个对象
    if need_del_sentence:
        db.session.delete(need_del_sentence)
        db.session.commit()

    return_message = {"code": True, "message": "Delete sentence success!"}

    return jsonify(return_message)


@app.route('/login', methods=['GET'])
def login():
    from s_database import User
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    user_info = User.query.filter_by(user_name=username).first()
    if user_info:
        if user_info.password == password:
            return_message = {"code": True, "message": "login success!"}
        else:
            return_message = {"code": False, "message": "Login failed!"}
    else:
        return_message = {"code": False, "message": "This user name {} does not exist!!!".format(str(username))}

    return jsonify(return_message)

# def encode_msg(data):】
#     """
#     :param data: In addition to general data types，you can pass a message object.
#     :return: json data
#     """
#
#     def convert_real_dict(object_dict):
#         return {key: value for key, value in object_dict.__dict_.item() if not key.startswith('_')}
#
#     if isinstance(data, object):
#         encode_func = convert_real_dict
#     elif isinstance(data, list):
#         encode_func = lambda list_obj: [convert_real_dict(item) for item in list_obj]
#
#     else:
#         encode_func = None
#
#     return json.dumps(data, encoding='utf-8', default=encode_func).replace("</", "<\\/")
#
#
# def decode_msg(json_data):
#     try:
#         return json.loads(json_data, encoding='utf-8')
#     except Exception:
#         print("WTF!!")


if __name__ == '__main__':
    app.run()
