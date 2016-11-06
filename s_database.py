#! /usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Grady'

from king import db

from config import TONGUE


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.user_name = username
        self.password = password


class Sentence(db.Model):
    sentence_id = db.Column(db.Integer, primary_key=True)
    chinese = db.Column(db.Text)
    english = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    type = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __init__(self, english, user_id, create_time, chinese="", type=TONGUE):
        self.chinese = chinese
        self.english = english
        self.user_id = user_id
        self.type = type
        self.create_time = create_time
