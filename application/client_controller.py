import requests
import base64
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjkfshkfksdjsfsjnjkb98899d9880sdfds*&^$#^'

FILE_PATH = 'C:/Users/Ravi/PycharmProjects/Flask/exam_portal_end_to_end/application/files/'


@app.route('/client/registration/', methods=['GET', 'POST'])
def client_registration():
    msg = ''
    if request.method == 'POST':
        reqdata = request.form
        if reqdata.get('username') and reqdata.get('name') and reqdata.get('email') and reqdata.get('password'):
            response = requests.post('http://localhost:5000/client/registration/',
                                     json={'username': reqdata.get('username'),
                                           'fullname': reqdata.get('name'),
                                           'email': reqdata.get('email'),
                                           'password': reqdata.get('password')})
            resp = response.json()
            if resp.get('success'):
                msg = resp.get('success')
            else:
                msg = resp.get('error')
        else:
            msg = 'Invalid credential..!'
    return render_template('client.html', resp=msg)


@app.route('/client/login/', methods=['GET', 'POST'])
def client_login():
    msg = ''
    if request.method == 'POST':
        reqdata = request.form
        if reqdata.get('username') and reqdata.get('password'):
            response = requests.post('http://localhost:5000/client/login/', json={'username': reqdata.get('username'),
                                                                                  'password': reqdata.get('password')})
            resp = response.json()
            if not resp.get('error') and resp.get('token'):
                session['client_user'] = reqdata.get('username')
                return render_template('data.html',token=resp.get('token'),file=resp.get('file'))
            elif resp.get('error') == 'Unauthorized access generate token ..!':
                return render_template('token_generate.html',token='',username=reqdata.get('username'),
                                       password=reqdata.get('password'))
            else:
                msg = resp.get('error')
        else:
            msg = 'Invalid credential..!'
    return render_template('client_login.html', resp=msg)



@app.route('/data/<token>', methods=['GET', 'POST'])
def decode_file(token):
    msg = ''
    if 'client_user' in session:
        if request.method == 'POST':
            print(request.form.get('file'))
            f_image = request.form.get('file')
            v = f_image.encode('utf-8')
            with open(FILE_PATH + session['client_user']+'.xlsx','wb') as file_save:
                file_image = base64.decodebytes(v)
                file_save.write(file_image)
            msg = request.form.get('file')
        return render_template('data.html', token=token,file = request.form.get('file'))
    return render_template('client_login.html')


@app.route('/upload/<token>', methods=['GET', 'POST'])
def upload_file(token):
    msg = ''
    if 'client_user' in session:
        if request.method == 'POST':
            file = request.files['file']
            file.save(FILE_PATH +session['client_user']+ '.xlsx')
            # if request.get('username') and request.get('password'):
            name = session['client_user']
            sdfile = {'file': open(FILE_PATH +session['client_user']+ '.xlsx', 'rb')}
            response = requests.post('http://localhost:5000/upload/questions/',
                                     files=sdfile,
                                     data={'name': name})
            resp = response.json()
            if resp.get('success'):
                return render_template('data.html', token=resp.get('success'))
            else:
                return render_template('data.html', token=resp.get('error'))
        return render_template('data.html', token=token)
    return render_template('client_login.html')

@app.route('/client/generate_token/',methods=['GET','POST'])
def token_generate():
    if request.method == 'POST':
        reqdata = request.form
        print(reqdata)
        if reqdata.get('username') and reqdata.get('password'):
            response = requests.patch('http://localhost:5000/client/token/', json={'username': reqdata.get('username'),
                                                                                  'password': reqdata.get('password')})
            resp = response.json()
            token = resp.get('success')
            return render_template('token_generate.html',token=token,username=reqdata.get('username'),
                                   password=reqdata.get('password'))
    return render_template('client_login.html',resp='')

@app.route('/client/logout/')
def client_logout():
    if 'client_user' in session:
        session.pop('client_user')
    return render_template('client_login.html')
