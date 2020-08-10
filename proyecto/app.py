from flask import Flask, render_template, request, url_for, redirect, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from camera import VideoCamera
import cv2

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)