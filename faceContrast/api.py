from flask import Flask,jsonify, request, redirect, render_template

from faceContrast.settings import * 

from faceContrast.contrast import Contrast




__all__ = ['app']

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/')
def index():
    return '<h2>人脸识别</h2>'


@app.route('/constract',methods=['GET','POST'])
def face_constract():
    """
    人脸识别
    """
    if request.method == 'POST':
        return Contrast().run()

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(port=5001)

