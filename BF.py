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
    __tablename__ = 'listen'
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

engine = create_engine("mysql+pymysql://root:lele@127.0.0.1:3306/flask", max_overflow=0, pool_size=5)
Session = sessionmaker(bind=engine)
session = Session()






########查查查查查查查查查查查查查查
@app.route("/user",methods=["POST","GET"])  # 只允许POST和GET
def hello():
    pageIndex = int(request.args["pageIndex"])  # 1
    pageSize = int(request.args.get("pageSize")) # 5
    msg = pageIndex*pageSize
    rets = session.query(Users).order_by(Users.id.desc())[msg - pageSize:msg]
    ret = session.query(Users).all()
    msg = len(ret)
    dic = {"total": msg}
    ls1 = []
    for i in rets:
        ls1.append(i.to_json())

    ls1.append(dic)
    return jsonify(ls1)


@app.route("/del",methods=["POST"])
def delete():
    id = request.get_json()["id"]
    msg = session.query(Users).filter(Users.id==id).delete()
    if msg:
        dic = {'state':True}
    else:
        dic = {'state':False}
    return jsonify(dic)


@app.route("/add",methods=["POST"])
def adds():

    res = request.get_json()

    obj1 = Users(name=res['name'], age=res["age"], address=res["address"], tel=res['tel'])
    if obj1:
        session.add(obj1)
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({"success": False})




########查查查查查查查查查查查查查查
@app.route("/link",methods=["POST","GET"])  # 只允许POST和GET
def links():
    rets = session.query(Link).order_by(Link.id.desc())
    if rets:
        ls1 = []
        for i in rets:
            ls1.append(i.to_json())
    else:
        ls1=[]
    return jsonify(ls1)



@app.route("/add_link",methods=["POST"])
def addlink():
    res = request.get_json()
    print(res)


    obj1 = Link(name=res['name'], link=res["link"])
    if obj1:
        session.add(obj1)
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({"success": False})





@app.route("/del_link",methods=["POST"])
def dellink():
    id = request.get_json()["id"]
    msg = session.query(Link).filter(Link.id==id).delete()
    if msg:
        dic = {'state':True}
    else:
        dic = {'state':False}
    return jsonify(dic)



#更新
@app.route("/edit_link",methods=["POST"])
def update():

    id = request.get_json()["id"]
    msg =  session.query(Link).filter(Link.id == id).first().to_json()
    dic = {}
    dic['name'] = msg['name']
    dic['link'] = msg['link']
    return jsonify({'state':True,'msg':dic})

@app.route("/update",methods=["POST"])
def edit():
    res = request.get_json()
    session.query(Link).filter(Link.id == res['id']).update({"name": res["name"],"link":res["link"]})
    session.commit()
    return jsonify({'success': True})
# @app.route('/')
# def init_db():
#     session.add_all([
#         Users(name="jiale"),
#         Users(name="alex"),
#     ])
#     session.commit()



session.close()

if __name__ == '__main__':
    app.run(debug=True,port=6666)




