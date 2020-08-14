from flask import Flask, Response, request, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 设置图片保存文件夹
UPLOAD_FOLDER = 'photo'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']


# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


# 上传图片
@app.route("/photo/upload", methods=['POST', "GET"])
def uploads():
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        file = request.files['file']
        if file and allowed_file(file.filename):
            print(file.filename)
            # secure_filename方法会去掉文件名中的中文
            file_name = secure_filename(file.filename)
            # 保存图片
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            return "success"
        else:
            return "格式错误，请上传jpg格式文件"
    return render_template('index.html')


# 查看图片
@app.route("/photo/<imageId>.jpg")
def get_frame(imageId):
    # 图片上传保存的路径
    with open(r'C:/Users/Administration/Desktop/photo_ceshi/photo/{}.jpg'.format(imageId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)