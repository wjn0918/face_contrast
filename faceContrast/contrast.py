"""
人像对比

"""
from flask import Flask,jsonify, request, redirect, render_template
from faceContrast.settings import * 
import face_recognition


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class Contrast():
    def __init__(self):
        pass

    def if_contain_face(self, file_stream):
        """
        识别图片中是否包含人脸
        """ 
        # Load the uploaded image file
        img = face_recognition.load_image_file(file_stream)
        # Get face encodings for any faces in the uploaded image
        unknown_face_encodings = face_recognition.face_encodings(img)
        if len(unknown_face_encodings) > 0:
            return unknown_face_encodings[0]
        else:
            return 0





    def __detect_faces_in_image(self, unknown_face_encoding):

        face_distances = face_recognition.face_distance(known_face_encodings, unknown_face_encoding)




    def __contrast(self):
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            flag = self.if_contain_face(file)
            if flag:
                print("图片中存在人脸")
                self.__detect_faces_in_image(flag)

                # return redirect(request.url)
            else:
                print("图片中没有人脸")
                return redirect(request.url)

            
        else:
            return redirect(request.url)


    def run(self):
        return self.__contrast()
        

        pass




