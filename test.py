from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
Base = declarative_base()

class Users(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    age = Column(Integer, default=18)
    address = Column(String(32))
    tel = Column(Integer)
    ctime = Column(DateTime, default=datetime.datetime.now)
    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
    __table_args__ = (
        # UniqueConstraint('id', 'name', name='uix_id_name'),
        # Index('ix_id_name', 'name', 'email'),
    )
engine = create_engine("mysql+pymysql://root:lele@127.0.0.1:3306/flask", max_overflow=0, pool_size=5)
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/user",methods=["POST","GET"])  # 只允许POST和GET
def hello():
    pageIndex = int(request.args["pageIndex"])  # 1
    pageSize = int(request.args.get("pageSize")) # 5
    msg = pageIndex*pageSize
    ret = session.query(Users).all()

    total = len(ret)
    if total==0:
        ls1 = []
        ls1.append({"total": total})
        return jsonify(ls1)
    else:
        # 升序
        # rets = session.query(Users)[msg-pageSize:msg]
        # 降序
        rets = session.query(Users).order_by(Users.id.desc())[msg - pageSize:msg]
        ls1 = []
        for i in rets:
            ls1.append(i.to_json())

        # dd = "Fri, Nov 09 2018 14:41:35 GMT"
        dd = "Wed, 22 Jul 2020 13:36:34 GMT"
        GMT_FORMAT = '%Y-%m-%d  %H:%M:%S'
        # timer = ls1[0]['ctime'].strftime('%Y-%m-%d %H:%M:%S') #datetime 转 str
        # print(datetime.datetime.strptime(timer,GMT_FORMAT))
        for i in ls1:
            i['ctime'] = i['ctime'].strftime('%Y-%m-%d %H:%M:%S')
            i['citme'] = datetime.datetime.strptime(i['ctime'], GMT_FORMAT)

        ls1.append({"total": total})
        return jsonify(ls1)

# ################ 添加 ################
@app.route("/add",methods=["POST"])
def add():
    res = request.get_json()
    print(res['name'])
    if res["age"]=="":
        res["age"] = 0
    if res["address"]=="":
        res["address"] ="未知"
    if res["tel"] =="":
        res["tel"] = 00
    obj1 = Users(name=res['name'],age=res["age"],address=res["address"],tel=res['tel'])
    if obj1:
        session.add(obj1)
        session.commit()
        return jsonify({'success':True})
    else:
        return jsonify({"success":False})

#删除
@app.route("/del",methods=["POST"])
def delete():
    id = request.get_json()["id"]
    session.query(Users).filter(Users.id==id).delete()
    session.commit()
    return jsonify({'state':True})


#更新
@app.route("/edit",methods=["POST"])
def update():
    id = request.get_json()["id"]
    msg =  session.query(Users).filter(Users.id == id).first().to_json()
    dic = {}
    dic['name'] = msg['name']
    dic['age'] = msg['age']
    dic['address'] = msg['address']
    dic['tel'] = msg['tel']

    return jsonify({'state':True,'msg':dic})

@app.route("/update",methods=["POST"])
def edit():
    res = request.get_json()
    print(res)
    session.query(Users).filter(Users.id == res['id']).update({"name": res["name"],"age":res["age"],"address":res["address"],"tel":res["tel"]})
    session.commit()
    return jsonify({'success': True})

# @app.route('/')
# def init_db():
#     """
#     根据类创建数据库表
#     :return:
#     """
#     engine = create_engine(
#         "mysql+pymysql://root:lele@127.0.0.1:3306/flask?charset=utf8",
#         max_overflow=0,  # 超过连接池大小外最多创建的连接
#         pool_size=5,  # 连接池大小
#         pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
#         pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
#     )
#     Base.metadata.create_all(engine)
#
#     return  '成功'
if __name__ == "__main__":
    app.run(port=6666,debug=True)