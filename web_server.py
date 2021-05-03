# -*- coding:utf-8 -*-
''' flask网页 '''

from QA_main import QuestionAnswerSystem
from flask import Flask, request, render_template, Response
import time
import json

app = Flask(__name__)


# 网页显示
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global handler
    global data_list

    if request.method == 'GET':
        return render_template('question_answer.html', answer={})
    else:
        question = request.form['key']
        if not question:
            return render_template('question_answer.html', answer={})
        start = time.time()
        answer = handler.question_answer_main(question)
        end = time.time()
        # 运行时间
        answer['time'] = '%.3f' % (end - start) + ' s'
        # 图谱数据
        data_list = answer['data_list']

        return render_template('question_answer.html', answer=answer)

# 传递图谱数据
@app.route('/tupu_data')
def tupu_data():
    global data_list
    return Response(json.dumps(data_list, ensure_ascii=False), mimetype='application/json')

# 程序入口
if __name__ == '__main__':
    data_list = []
    handler = QuestionAnswerSystem()
    app.run(debug=True, port=5000)
