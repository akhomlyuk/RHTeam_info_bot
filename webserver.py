from flask import Flask, render_template, request
from config import *
from brief import *
from icecream import ic
import logging

app = Flask(__name__, template_folder=r'templates/')
logging.basicConfig(level=logging.INFO, filename='logs/flask.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@app.route('/')
def index():
    with open('notes/next', 'r', encoding='UTF-8', newline='') as file:
        content = file.read()
    with open('notes/todo', 'r', encoding='UTF-8', newline='') as todo:
        todo = todo.read()
    return render_template('index.html', next_event=content, todo_list=todo)


@app.route('/nextevent', methods=['POST'])
def save_nextevent():
    updated_content = request.form['next_event']
    with open('notes/next', 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html')


@app.route('/todolist', methods=['POST'])
def save_todolist():
    updated_content = request.form['todo_list']
    with open('notes/todo', 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html')


@app.route('/settings')
def show_settings():
    # with open('config.py', 'r', encoding='UTF-8', newline='') as file:
    #     content = file.read()
    return render_template('settings.html', content=brief)


#
#
# @app.route('/update_commands', methods=['POST'])
# def update_commands():
#     new_cmd = request.form['cmd']
#
#     return redirect('/settings')


if __name__ == "__main__":
    ic(app.run(host='0.0.0.0', port=3000))
