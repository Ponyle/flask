from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
import datetime
from sqlalchemy import create_engine,or_,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary, BLOB, Text, ForeignKey, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'userinfo'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(32))
    user_type = Column(String(32))
    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

class Users(Base):
    __tablename__ = 'listen'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    age = Column(Integer, default=18)
    address = Column(String(32))
    img_name = Column(String(32))
    img_status = Column(String(32))
    tel = Column(Integer)
    username = Column(String(32))
    password = Column(String(32))
    ctime = Column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Link(Base):
    __tablename__ = 'link'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    link = Column(String(32))
    ctime = Column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(String(32))
    sort_id = Column(String(32))
    desc = Column(String(6666))
    author = Column(String(32))
    ctime = Column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


engine = create_engine("mysql+pymysql://root:lele@127.0.0.1:3306/flask", max_overflow=0, pool_size=5)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    """
    根据类创建数据库表
    :return:
    """
    engine = create_engine(
        "mysql+pymysql://root:lele@127.0.0.1:3306/flask?charset=utf8",
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )

    Base.metadata.create_all(engine)

@app.route('/total', methods=["GET"])
def totals():
    total = session.query(Users).count()
    return jsonify(total)



@app.route("/login_auth",methods=["POST","GET"])
def login():
    res = request.get_json()
    msg = session.query(User).filter(and_(User.username == res['username'],User.password == res['password'])).first()
    if msg !=None:
        if msg.to_json()!=None:
            return jsonify({'state':True,'user_type':msg.to_json()['user_type']})
        else:
            return jsonify({'state': False})
    else:
        return jsonify({'state': False})



########查查查查查查查查查查查查查查
@app.route("/user", methods=["POST", "GET"])  # 只允许POST和GET
def hello():
    pageIndex = int(request.args["pageIndex"])  # 1
    pageSize = int(request.args.get("pageSize"))  # 5
    msg = pageIndex * pageSize
    rets = session.query(Users).order_by(Users.id.desc())[msg - pageSize:msg]
    ret = session.query(Users).all()
    # msg = len(ret)
    # dic = {"total": msg}
    ls1 = []
    for i in rets:
        ls1.append(i.to_json())

    # ls1.append(dic)
    return jsonify(ls1)


@app.route("/del", methods=["POST"])
def delete():
    id = request.get_json()["id"]
    msg = session.query(Users).filter(Users.id == id).delete()
    if msg:
        dic = {'state': True}
    else:
        dic = {'state': False}
    return jsonify(dic)


@app.route("/add", methods=["POST"])
def adds():
    res = request.get_json()
    obj1 = Users(name=res['name'], age=res["age"], address=res["address"], tel=res['tel'], img_name=res['img_name'],
                 img_status=res['status'])
    if obj1:
        session.add(obj1)
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({"success": False})


########查查查查查查查查查查查查查查
@app.route("/link", methods=["POST", "GET"])  # 只允许POST和GET
def links():
    rets = session.query(Link).order_by(Link.id.desc())

    if rets:
        ls1 = []
        for i in rets:
            ls1.append(i.to_json())
    else:
        ls1 = []
    return jsonify(ls1)


@app.route("/add_link", methods=["POST"])
def addlink():
    res = request.get_json()

    obj1 = Link(name=res['name'], link=res["link"])
    if obj1:
        session.add(obj1)
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({"success": False})


@app.route("/del_link", methods=["POST"])
def dellink():
    id = request.get_json()["id"]
    msg = session.query(Link).filter(Link.id == id).delete()
    if msg:
        dic = {'state': True}
    else:
        dic = {'state': False}
    return jsonify(dic)


# 更新

@app.route("/edit_listen", methods=["POST"])
def updates():
    id = request.get_json()["id"]
    msg = session.query(Users).filter(Users.id == id).first().to_json()
    dic = {}
    dic['name'] = msg['name']
    dic['age'] = msg['age']
    dic['address'] = msg['address']
    dic['tel'] = msg['tel']
    dic['img_name'] = msg['img_name']
    dic['img_status'] = msg['img_status']

    return jsonify({'state': True, 'msg': dic})


@app.route("/update_listen", methods=["POST"])
def edits():
    res = request.get_json()
    if res['img_name'] == "":
        res['img_name'] = res['img_status']

    session.query(Users).filter(Users.id == res['id']).update(
        {"img_status": res['img_status'], "name": res["name"], "address": res["address"], "tel": res["tel"],
         "img_name": res["img_name"], "age": res["age"]})

    session.commit()
    return jsonify({'success': True})


@app.route("/edit_link", methods=["POST"])
def update():
    id = request.get_json()["id"]
    msg = session.query(Link).filter(Link.id == id).first().to_json()
    dic = {}
    dic['name'] = msg['name']
    dic['link'] = msg['link']
    return jsonify({'state': True, 'msg': dic})


@app.route("/update", methods=["POST"])
def edit():
    res = request.get_json()
    session.query(Link).filter(Link.id == res['id']).update({"name": res["name"], "link": res["link"]})
    session.commit()
    return jsonify({'success': True})


# @app.route('/')
# def init_db():
#     session.add_all([
#         Users(name="jiale"),
#         Users(name="alex"),
#     ])
#     session.commit()
import datetime
import random


@app.route('/imglink', methods=['GET', 'POST'])
def img():
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = basedir + "\static"
    img = request.files.get('file')
    upload_path = os.path.join(basedir, 'static/images', img.filename)
    img.save(upload_path)
    return '添加成功'
##################

# #####################文章

#添加文章
@app.route("/add_article", methods=["POST"])
def addarticle():
    res = request.get_json()
    obj1 = Article(title=res['title'], sort_id=res["sort_id"], desc=res['desc'], author=res['author'])
    if obj1:
        session.add(obj1)
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({"success": False})

#初始化文章
@app.route("/init_article", methods=["POST", "GET"])  # 只允许POST和GET
def init():
    # pageIndex = int(request.args["pageIndex"])  # 1
    # pageSize = int(request.args.get("pageSize")) # 5
    # msg = pageIndex*pageSize
    # rets = session.query(Users).order_by(Users.id.desc())[msg - pageSize:msg]
    rets = session.query(Article).order_by(Article.id.desc())
    ls1 = []
    for i in rets:
        ls1.append(i.to_json())
    return jsonify(ls1)

#预览
@app.route("/preview_article", methods=["POST"])
def preview():
    id = request.get_json()["id"]

    msg = session.query(Article).filter(Article.id == id).first().to_json()
    dic = {}
    dic['title'] = msg['title']
    dic['sort_id'] = msg['sort_id']
    dic['desc'] = msg['desc']
    dic['author'] = msg['author']
    dic['ctime'] = msg['ctime']
    return jsonify({'state': True, 'msg': dic})

#文章图片地址
@app.route('/img_article', methods=['GET', 'POST'])
def imgarticle():
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = basedir + "\static"
    img = request.files.get('file')
    upload_path = os.path.join(basedir, 'static/news_img', img.filename)
    img.save(upload_path)
    return img.filename

#文章编辑
@app.route("/edit_article", methods=["POST"])
def editarticle():
    id = request.get_json()["id"]
    msg = session.query(Article).filter(Article.id == id).first().to_json()
    dic = {}
    dic['title'] = msg['title']
    dic['sort_id'] = msg['sort_id']
    dic['desc'] = msg['desc']
    dic['author'] = msg['author']
    return jsonify({'state': True, 'msg': dic})

#文章更新
@app.route("/update_article", methods=["POST"])
def updatearticle():
    res = request.get_json()
    session.query(Article).filter(Article.id == res['id']).update(
        {'title':res['title'],'sort_id':res['sort_id'],'desc':res['desc']})
    session.commit()
    return jsonify({'success': True})

#文章图片地址
@app.route('/media_article', methods=['GET', 'POST'])
def mediaarticle():
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = basedir + "\static"
    meida = request.files.get('file')
    upload_path = os.path.join(basedir, 'static/media', meida.filename)
    meida.save(upload_path)
    return meida.filename

session.close()
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8888)
