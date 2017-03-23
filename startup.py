from flask import Flask, render_template, request, flash, redirect
from flask_bootstrap import Bootstrap
from tinydb import TinyDB
import functools

app = Flask(__name__)
Bootstrap(app)

db = TinyDB('database.json')
tabela = db.table("investimentos")
app.secret_key = 'some_secret'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/investir", methods=("POST",))
def investir():
    dados = {
        'nome': request.form.get("nome"),
        'patrulha': request.form.get("patrulha"),
        'zumbi': request.form.get("zumbi"),
        'olimpiadas': request.form.get("olimpiadas"),
    }
    tabela.insert(dados)
    flash("Obrigado pelo seu investimento!")
    return redirect("/")


@app.route("/investido")
def investidos():
    total_zumbi = functools.reduce(lambda x, y: x+y, [int(x['zumbi']) for x in tabela.all()])
    total_olimpiadas = functools.reduce(lambda x, y: x+y, [int(x['olimpiadas']) for x in tabela.all()])
    return render_template("resultados.html", total_zumbi=total_zumbi,
        total_olimpiadas=total_olimpiadas, votos=tabela.all())
