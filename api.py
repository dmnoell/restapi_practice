from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)


class PokeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))

with app.app_context():
    db.create_all()

argument_values = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='name is required')
parser.add_argument('type', type=str, required=True, help='type is required')

class AllPokemon (Resource):
    def get(self):
        pokemon = PokeModel.query.all()
        pokelist = {}
        for poke in pokemon:
            pokelist[poke.id] = {'name': poke.name, 'type': poke.type}
        return pokelist

class Pokemon (Resource):
    @marshal_with(argument_values)
    def get(self, pokemon_id):
        pokemon = PokeModel.query.filter_by(id=pokemon_id).first()
        if not pokemon:
            abort(409, message='no pokemon with that id')
        return pokemon

    @marshal_with(argument_values)    
    def post(self, pokemon_id):
        args = parser.parse_args()
        pokemon = PokeModel.query.filter_by(id=pokemon_id).first()
        if pokemon:
            abort(409, message='Pokemon with the same id already exists')
        new_pokemon = PokeModel(id=pokemon_id, name=args['name'], type=args['type'])
        db.session.add(new_pokemon)
        db.session.commit()
        return new_pokemon, 200
    
    @marshal_with(argument_values)
    def put(self, pokemon_id):
        args = parser.parse_args()
        pokemon = PokeModel.query.filter_by(id=pokemon_id).first()
        if not pokemon:
            abort(404, message='pokemon not found')
        if args['name']:
            pokemon.name = args['name']
        if args['type']:
            pokemon.type = args['type']
        db.session.commit()
        return pokemon
    
    @marshal_with(argument_values)
    def delete(self, pokemon_id):
        pokemon = PokeModel.query.filter_by(id=pokemon_id).first()
        if not pokemon:
            abort(404, message='pokemon not found')
        db.session.delete(pokemon)
        db.session.commit()
        return "sucessful delete", 200






api.add_resource(Pokemon, '/pokemon/<int:pokemon_id>')
api.add_resource(AllPokemon, '/pokemon')

if __name__ == '__main__':
    app.run(debug=True)

