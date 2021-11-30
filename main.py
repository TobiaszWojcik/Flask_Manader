from flask import Flask, render_template
from actions import Manager
from actions import Account

acc = Account()
manager = Manager()

acc.get_file_path('./in.txt')
acc.import_db()

app = Flask(__name__)

@app.route("/")
def mainpage():
    content = {
        'title': 'Strona główna',
        'products': list(acc.stan_magazynowy.keys())
    }

    return render_template('index.html', contents=content)

@app.route("/history")
def historypage():
    content = {
        'title': 'Historia'
    }
    return render_template('history.html', contents=content)

if __name__  == '__main__':
    app.run(debug=True)