from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# 定义ORM

#定义账号密码表
class User(db.Model):
  __tablename__ = 'user_mm'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(100), nullable=False)
  mm = db.Column(db.String(1000), nullable=False)

  def __init__(self, username, mm):
    self.username = username
    self.mm = mm

#定义原始记录表
class Ystable(db.Model):
  __tablename__ = 'yuanshi'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  date = db.Column(db.String(1000), nullable=False)  #记录时间
  name = db.Column(db.String(1000), nullable=False)  #名字
  num = db.Column(db.String(1000), nullable=False)   #数量
  site = db.Column(db.String(1000), nullable=False)  #位置

  def __init__(self, date, name,num,site):
    self.date = date
    self.name = name
    self.num = num
    self.site = site

#定义登记记录表
class Jltable(db.Model):
  __tablename__ = 'jilu'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  date = db.Column(db.String(1000), nullable=False)  #记录时间
  name = db.Column(db.String(1000), nullable=False)  #名字
  num = db.Column(db.String(1000), nullable=False)   #数量
  site = db.Column(db.String(1000), nullable=False)  #位置
  people = db.Column(db.String(1000), nullable=False)  #记录人
  in_out = db.Column(db.String(1000), nullable=False)  # 出入库

  def __init__(self, date, name,num,site,people,in_out):
    self.date = date
    self.name = name
    self.num = num
    self.site = site
    self.people = people
    self.in_out = in_out
