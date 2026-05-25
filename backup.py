from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = '4e726b35e1357a835279f6014abd33a07fe6a3575f0a43ae'

usuarios = {
    "Kaiky": {"senha": "1604", "permissao": "gerente"},
    "Caixa1": {"senha": "1111", "permissao": "caixa"},
    "Atendente1": {"senha": "2222", "permissao": "atendente"},
    "Cozinha1": {"senha": "3333", "permissao": "cozinha"}
}

mesas = {
    i: {"status": "Livre", "pedidos": [], "total": 0.0, "forma_pagamento": None, "responsavel": None}
    for i in range(1, 11)
}

cardapio = {
    'hamburgueres': [{'nome': 'X-Burger', 'preco': 18.00}, {'nome': 'X-Bacon', 'preco': 22.00}],
    'bebidas': [{'nome': 'Refrigerante Lata', 'preco': 6.00}, {'nome': 'Suco Natural', 'preco': 8.00}],
    'acompanhamentos': [{'nome': 'Batata Frita', 'preco': 10.00}, {'nome': 'Onion Rings', 'preco': 12.00}, {'nome': 'Batata Frita Especial', 'preco': 16.00}]
}

@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', usuario=session['usuario'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        if nome in usuarios and usuarios[nome]['senha'] == senha:
            session['usuario'] = nome
            session['permissao'] = usuarios[nome]['permissao']
            flash(f"Bem-vindo, {nome}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Usuário ou senha inválidos!", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sessão encerrada.", "info")
    return redirect(url_for('login'))

@app.route('/mesas')
def ver_mesas():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('mesas.html', mesas=mesas)

@app.route('/mesa/<int:numero>', methods=['GET', 'POST'])
def gerenciar_mesa(numero):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    mesa = mesas.get(numero)
    if not mesa:
        flash("Mesa não encontrada!", "danger")
        return redirect(url_for('ver_mesas'))

    if request.method == 'POST':
        item = request.form['item']
        try:
            valor = float(request.form['valor'])
        except ValueError:
            flash("Valor inválido!", "danger")
            return redirect(url_for('gerenciar_mesa', numero=numero))
        mesa['pedidos'].append({"item": item, "valor": valor})
        mesa['total'] += valor
        mesa['status'] = "Ocupada"
        mesa['responsavel'] = session['usuario']
        flash(f"{item} adicionado com sucesso!", "success")

    return render_template('gerenciar_mesa.html', numero=numero, mesa=mesa, cardapio=cardapio)

@app.route('/cozinha')
def cozinha():
    pedidos = []

    for numero, mesa in mesas.items():
        for index, pedido in enumerate(mesa['pedidos']):
            pedidos.append({
                "mesa": numero,
                "item": pedido['item'],
                "index": index
            })

    return render_template('cozinha.html', pedidos=pedidos)

@app.route('/abrir_caixa', methods=['GET', 'POST'])
def abrir_caixa():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        valor = float(request.form['valor'])

        flash(f"Caixa aberto com R$ {valor:.2f}", "success")

        return redirect(url_for('index'))

    return render_template('abrir_caixa.html')

@app.route('/fechar_caixa', methods=['GET', 'POST'])
def fechar_caixa():

    recebimentos = {
        "Dinheiro": 0,
        "Cartão Débito": 0,
        "Cartão Crédito": 0,
        "Pix": 0
    }

    dinheiro_em_caixa = 0

    if request.method == 'POST':
        flash("Caixa fechado com sucesso!", "success")
        return redirect(url_for('index'))

    return render_template(
        'fechar_caixa.html',
        recebimentos=recebimentos,
        dinheiro_em_caixa=dinheiro_em_caixa
    )

@app.route('/pedido_pronto/<int:mesa>/<int:index>', methods=['POST'])
def pedido_pronto(mesa, index):

    if mesa in mesas:
        try:
            mesas[mesa]['pedidos'].pop(index)

            if not mesas[mesa]['pedidos']:
                mesas[mesa]['status'] = "Livre"
                mesas[mesa]['total'] = 0

            flash("Pedido finalizado!", "success")

        except IndexError:
            flash("Pedido não encontrado!", "danger")

    return redirect(url_for('cozinha'))

if __name__ == '__main__':
    app.run(debug=True)