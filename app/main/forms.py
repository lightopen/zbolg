# coding=utf-8
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required, Length
import random

class PushMsgForm(Form):
    message = TextAreaField('message:', validators=[Required(), Length(1, 144)])
    submit = SubmitField("留言")

class CommentForm(Form):
    values_list = ['你觉得这是谁的日志？','回头看大学日志是不是很矫情？','好起嘞～','说点什么吧?']    
    comment = TextAreaField('',default=values_list[random.randint(0,3)], validators=[Required()])
    submit = SubmitField("评论")