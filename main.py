from flask import Flask, render_template, request, url_for
from actions import Manager
from actions import Account

acc = Account()
manager = Manager()


acc.get_file_path('./in.txt')
acc.import_db()


@manager.assign('sprzedaz')
def sprzedaz():
    return acc.sprzedaz(request.form['product'], int(request.form['price']), int(request.form['pices']))


@manager.assign('zakup')
def zakup():
    return acc.zakup(request.form['product'], int(request.form['price']), int(request.form['pices']))


@manager.assign('saldo')
def saldo():
    return acc.saldo(int(request.form['wartosc']), request.form['comment'])


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def mainpage():
    error = None
    if request.method == 'POST':
        odp = manager.execute(request.form['action'])
        if odp[0]:
            acc.update_db()
        else:
            error = odp[1]
    print(error)
    content = {
        'error': error,
        'stan': acc.saldo_kwota,
        'title': 'Strona główna',
        'products': acc.stan_magazynowy
    }
    return render_template('index.html', contents=content)


@app.route('/history/<linefrom>/<lineto>')
def historypage(linefrom=0, lineto=0):
    line_from = int(linefrom)
    line_to = int(lineto)
    history = acc.przeglad(line_from, line_to)
    content = {
        'title': 'Historia',
        'history': history
    }
    print(content)
    return render_template('history.html', contents=content)


if __name__ == '__main__':
    app.run(debug=True)
