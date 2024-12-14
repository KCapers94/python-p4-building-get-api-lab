#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():

    bakers = [baker.to_dict() for baker in Bakery.query.all()]

    response = make_response(
        bakers,
        200
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    baker = Bakery.query.filter(Bakery.id == id).first()

    baker_dict = baker.to_dict()

    response = make_response(
        baker_dict,
        200,
        {"Content-Type": "application/json"}
    )

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    
    
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    baked_good_dict = [baked_good.to_dict() for baked_good in baked_goods]

    response = make_response (
        baked_good_dict,
        200
    )

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():

    baked = BakedGood.query.order_by(desc(BakedGood.price)).first()

    if baked:
        baked_good_dict = baked.to_dict()
    else:
        baked_good_dict = {}

    response = make_response(
        jsonify(baked_good_dict),
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
