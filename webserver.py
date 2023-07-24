from flask import Flask, render_template, request, redirect
from config import *
from brief import *
app = Flask(__name__, template_folder=r'templates/')


@app.route('/')
def index():
    with open('notes/next', 'r', encoding='UTF-8', newline='') as file:
        content = file.read()
    return render_template('index.html', content=content)


@app.route('/save', methods=['POST'])
def save():
    updated_content = request.form['content']
    with open('notes/next', 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return 'Файл сохранен успешно. <a href="/">Вернуться на главную</a>'


@app.route('/settings')
def show_settings():
    # with open('config.py', 'r', encoding='UTF-8', newline='') as file:
    #     content = file.read()
    return render_template('settings.html', token=results_cmds, content=brief)
#
#
# @app.route('/update_commands', methods=['POST'])
# def update_commands():
#     new_cmd = request.form['cmd']
#
#     return redirect('/settings')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

