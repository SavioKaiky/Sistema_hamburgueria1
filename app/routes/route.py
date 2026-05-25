from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os

from app.models.usuario import Usuario
from app import db

# imports de permição de usuarios
from app.utils.decorators import login_obrigatorio
from app.utils.decorators import requer_permissao

# imports das rotas da mesa
from app.models.mesa import Mesa
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido

route = Blueprint("route", __name__)
# Cardapio temporario(Apenas para testes, depois será retirado do código e colocado no banco de dados)
cardapio = {
    'hamburgueres': [{'nome': 'X-Burger', 'preco': 18.00}, {'nome': 'X-Bacon', 'preco': 22.00}],
    'bebidas': [{'nome': 'Refrigerante Lata', 'preco': 6.00}, {'nome': 'Suco Natural', 'preco': 8.00}],
    'acompanhamentos': [{'nome': 'Batata Frita', 'preco': 10.00}, {'nome': 'Onion Rings', 'preco': 12.00}, {'nome': 'Batata Frita Especial', 'preco': 16.00}]
}

@route.route('/mesas')
@login_obrigatorio
@requer_permissao("gerente", "caixa", "atendente")

def ver_mesas():
    mesas = Mesa.query.order_by(Mesa.numero).all()
    if 'usuario' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('mesas.html', mesas=mesas)

@route.route('/mesa/<int:numero>', methods=['GET', 'POST'])
@login_obrigatorio
@requer_permissao("gerente", "caixa", "atendente")

def gerenciar_mesa(numero):

    mesa = Mesa.query.filter_by(numero=numero).first()

    if not mesa:
        flash("Mesa não encontrada!", "danger")
        return redirect(url_for('ver_mesas'))
    pedido = Pedido.query.filter_by(mesa_id=mesa.id).filter(Pedido.status != "finalizado").first()

    if not pedido:
        pedido = Pedido(mesa_id=mesa.id,status="recebido")
        db.session.add(pedido)
        mesa.status = "ocupada"
        db.session.commit()

    if request.method == 'POST':
        item_nome = request.form['item']
        try:
            valor = float(request.form['valor'])
        except ValueError:
            flash("Valor inválido!", "danger")
            return redirect(url_for('gerenciar_mesa',numero=numero))
        item = ItemPedido(pedido_id=pedido.id,nome=item_nome,preco=valor,quantidade=1)
        db.session.add(item)
        pedido.total += valor
        mesa.status = "ocupada"
        db.session.commit()
        flash(f"{item_nome} adicionado com sucesso!","success")
        return redirect(
            url_for('route.gerenciar_mesa', numero=numero))
    
    itens = ItemPedido.query.filter_by(pedido_id=pedido.id).all()
    return render_template('gerenciar_mesa.html', numero=numero, mesa=mesa, pedido=pedido, itens=itens, cardapio=cardapio)

@route.route('/cozinha')
@login_obrigatorio
@requer_permissao("gerente", "cozinha")

def cozinha():
    pedidos = []

    # for numero, mesa in mesas.items():
    #     for index, pedido in enumerate(mesa['pedidos']):
    #         pedidos.append({
    #             "mesa": numero,
    #             "item": pedido['item'],
    #             "index": index
    #         })

    return render_template('cozinha.html', pedidos=pedidos)

@route.route('/abrir_caixa', methods=['GET', 'POST'])
@login_obrigatorio
@requer_permissao("gerente", "caixa")

def abrir_caixa():

    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        valor = float(request.form['valor'])

        flash(f"Caixa aberto com R$ {valor:.2f}", "success")

        return redirect(url_for('index'))

    return render_template('abrir_caixa.html')

@route.route('/fechar_caixa', methods=['GET', 'POST'])
@login_obrigatorio
@requer_permissao("gerente", "caixa")

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

@route.route('/pedido_pronto/<int:mesa>/<int:index>', methods=['POST'])
@login_obrigatorio
@requer_permissao("gerente", "cozinha")

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