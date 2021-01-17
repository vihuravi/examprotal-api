import requests
from exam_portal_end_to_end.application.question import Question
from exam_portal_end_to_end.application.client_controller import app, request, render_template, redirect, url_for, session

app.config['SECRET_KEY'] = 'HFKJSFHOUSOPOWIPWOUWOURWR8R939835*&^$#^'

def deserialize_questions(data):
    qlist = []
    for que in data:
        qlist.append(Question(que.get('Qid'),
                              que.get('Question'),
                              que.get('Qop1'), que.get('Qop2'), que.get('Qop3'),
                              que.get('Qop4'), que.get('Qans')))
    return qlist

@app.route('/student/registration/', methods=['GET', 'POST'])
def student_registration():
    msg = ''
    if request.method == 'POST':
        reqdata = request.form
        if reqdata.get('username') and reqdata.get('name') and reqdata.get('email') and reqdata.get('password') and reqdata.get('clid'):
            response = requests.post('http://localhost:5000/student/registration/',
                                     json={'username': reqdata.get('username'),
                                           'fullname': reqdata.get('name'),
                                           'email': reqdata.get('email'),
                                           'password': reqdata.get('password'),
                                           'employer id': reqdata.get('clid')})
            resp = response.json()
            if resp.get('success'):
                msg = resp.get('success')
            else:
                msg = resp.get('error')
        else:
            msg = 'Invalid credential..!'
    return render_template('student.html', resp=msg)

@app.route('/student/login/', methods=['GET', 'POST'])
def student_login():
    msg = ''
    if request.method == 'POST':
        reqdata = request.form
        if reqdata.get('username') and reqdata.get('password'):
            response = requests.post('http://localhost:5000/student/login/', json={'username': reqdata.get('username'),
                                                                                   'password': reqdata.get('password')})
            resp = response.json()
            if resp.get('success'):
                session['userinfo'] = reqdata.get('username')
                return redirect(url_for('question_sheet', clid=resp.get('success')))
            else:
                msg = resp.get('error')
        else:
            msg = 'Invalid credential..!'
    return render_template('student_login.html', resp=msg)


def final_calculation(answers,q_answer):
    count = 0
    # print('stud --',answers.get('0'))
    # print('orginal--',q_answer[0].qusAns)
    for i in range(len(answers)):
        if answers.get(str(i)) == q_answer[i].qusAns:
            count = count + 1
    return count


@app.route('/student/question/<clid>', methods=['GET', 'POST'])
def question_sheet(clid):
    if 'userinfo' in session:
        if request.method == 'GET':
            response = requests.get('http://localhost:5000/student/question/', json={'clientid': clid})
            questions = deserialize_questions(response.json().get('success'))
            line = [i for i in range(len(questions) - 1)]
            return render_template('questions.html', questionlist=questions, l=line, clid=clid)
        else:
            data = request.form
            response = requests.get('http://localhost:5000/student/question/', json={'clientid': clid})
            questions = deserialize_questions(response.json().get('success'))
            mark = final_calculation(data, questions)
            print(mark)
            line = [i for i in range(len(questions) - 1)]
            return redirect(url_for('final_ans',mark=mark))
    return render_template('student_login.html')

@app.route('/student/score/<mark>', methods=['GET', 'POST'])
def final_ans(mark):
    if 'userinfo' in session:
        return render_template('mark.html', mark=mark)
    return render_template('student_login.html')

@app.route('/student/logout/')
def student_logout():
    if 'userinfo' in session:
        session.pop('userinfo')
    return render_template('student_login.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
