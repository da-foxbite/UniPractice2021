from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
# from flask_swagger import swagger

app = Flask(__name__)

# 'sqlite:///db.sqlite' |'sqlite:///db.db' ???
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True, nullable=False)
  amount = db.Column(db.Integer, nullable=False)
  add_notes = db.Column(db.String(200))

  def __init__(self, name, amount, add_notes):
    self.name = name
    self.amount = amount
    self.add_notes = add_notes

# Schema
class ItemSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'amount', 'add_notes')

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# db.create_all()
# >> from apptest import db
# >> db.create_all()
# >> exit()

# test, попробовать подключить сваггер
@app.route('/', methods=['GET'])
def get_hello():
#  return jsonify({'msg': 'Проверка работоспособности: OK'})
  return 'Проверка работоспособности: OK'



# GET *
# /item или /items ??
@app.route('/item', methods=['GET'])
def get_items():
    all_items = Item.query.all()
    return items_schema.jsonify(all_items)

# GET
# <int:id> ?
@app.route('/item/<id>', methods=['GET'])
def get_item(id):
  item = Item.query.get(id)
  return item_schema.jsonify(item)

# POST
@app.route('/item', methods=['POST'])
def add_item():
  name = request.json['name']
  amount = request.json['amount']
  add_notes = request.json['add_notes']
  new_item = Item(name, amount, add_notes)
  db.session.add(new_item)
  db.session.commit()
  return item_schema.jsonify(new_item), 201

# DELETE
@app.route('/item/<id>', methods=['DELETE'])
def delete_item(id):
  item = Item.query.get(id)
  db.session.delete(item)
  db.session.commit()
  return item_schema.jsonify(item), 204

# PUT
@app.route('/item/<id>', methods=['PUT'])
def update_item(id):
  item = Item.query.get(id)
  name = request.json['name']
  amount = request.json['amount']
  add_notes = request.json['add_notes']
  item.name = name
  item.amount = amount
  item.add_notes = add_notes
  db.session.commit()
  return item_schema.jsonify(item)

@app.errorhandler(404)
def not_found(error):
  return jsonify({'msg': 'ERROR: Resource not found'}), 404

@app.errorhandler(500)
def not_found(error):
  return jsonify({'msg': 'ERROR: Server error'}), 500

if __name__ == '__main__':
  app.run(debug=True)
