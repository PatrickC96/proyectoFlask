from flask import Flask, render_template, request, url_for, redirect, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from camera import VideoCamera

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

video_camera = None
global_frame = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/administrador')
def administrador():
    data = ['1','2','3','4']
    return render_template('administrador.html',contacts = data)

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')
    
@app.route('/graficos')
def graficos():
    return render_template('graficos.html')


@app.route('/build_plot')
def build_plot():

    img = io.BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)
    return img.getvalue()


@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)