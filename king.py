import logging
import os

from flask import Flask
from flask import request
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from config import TONGUE
from attr import attrs, attrib
import attr

app = Flask(__name__)
# app.jinja_env.variable_start_string = '{{ '
# app.jinja_env.variable_end_string = ' }}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format("kos.db")
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = b'\xce+#\xf7\x87g\xfe\r\xd1D\xec3\xce4\x7f\t\t+A]\xdb\xaf!VD\x13\xdb&&3\xe8\xbav\x98oG\xa9\xcd\xc8\x15\xbc\xd4m%[X\xc4\xd2\x1f&\xbd\x1aN\xb0%\x01\x10\xeb\xd0\xb1y\xf9\x96='
db = SQLAlchemy(app)

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


@attrs
class ReturnInfo(object):
    code = attrib(default=False)
    message = attrib(default='')


class ReturnAddInfo(ReturnInfo):
    sentence_id = attrib(default=-1)


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
        return_message = ReturnAddInfo()

        if 'chinese' in request.json and 'english' in request.json \
                and 'create_time' in request.json:
            user_id = Sentence.query.filter_by(user_name=username).first()
            if user_id:
                user_id = user_id.user_id
                new_sentence = Sentence(request.json['english'], user_id,
                                        datetime.utcnow(), request.json['chinese'],
                                        TONGUE)
                db.session.add(new_sentence)
                db.session.commit()
                return_message.code = True
                return_message.message = "Add success!"
                return_message.sentence_id = new_sentence.sentence_id
            else:
                return_message.message = "This user name does not exist!"

        else:
            return_message.message = "argument is wrong!"

        return jsonify(attr.asdict(return_message))
    else:
        return "ERROR!!!"


@app.route('/<username>/items/<sentence_id>', methods=['DELETE'])
def delete_sentence(username, sentence_id):
    from s_database import Sentence
    return_message = ReturnInfo()
    delete_result = Sentence.query.filter_by(sentence_id=sentence_id).delete()
    db.session.commit()
    if delete_result:
        return_message.code = True
        return_message.message = "Delete sentence success!"
    else:
        logging.error("internal db error")
        return_message.message = "internal db error!"
    return jsonify(attr.asdict(return_message))


@app.route('/login', methods=['GET'])
def login():
    from s_database import User
    return_message = ReturnInfo()
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    user_info = User.query.filter_by(user_name=username).first()
    if user_info:
        if user_info.password == password:
            return_message.code = True
            return_message.message = "Login success!"
        else:
            return_message.message = "Login failed!"
    else:
        return_message.message = "This user name {} does not exist!!".format(str(username))

    return jsonify(attr.asdict(return_message))

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
