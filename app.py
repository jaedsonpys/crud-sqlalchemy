from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

database_file = 'sqlite:///mydatabase.db'

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)


def object_to_dict(obj) -> dict:
    return dict(obj)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(50))
    age = db.Column(db.Integer)


class UserAPI(Resource):
    @staticmethod
    def get():
        all_users = []
        for row in Users.query.all():
            user = {
                'name': row.name,
                'email': row.email,
                'age': row.age
            }

            all_users.append(user)

        return all_users

    @staticmethod
    def post():
        data: dict = request.json

        user_name = data.get('name')
        user_email = data.get('email')
        user_age = data.get('age')

        if not all([user_name, user_email, user_age]):
            return {'error': 'Invalid data'}, 400

        user = Users(name=user_name, email=user_email, age=user_age)
        db.session.add(user)
        db.session.commit()

        return {'status': 'created'}, 201

    @staticmethod
    def put():
        email = request.args.get('email')
        data: dict = request.json

        if not data or not email:
            return {'error': 'Invalid data/args'}, 400

        user = Users.query.filter_by(email=email).first()
        if not user:
            return {'error': 'Inexistent user'}, 400

        for key, value in data.items():
            if key == 'name':
                user.name = value
            elif key == 'email':
                user.email = value
            elif key == 'age':
                user.age = value

        db.session.commit()
        return 'OK', 200

    @staticmethod
    def delete():
        email = request.args.get('email')

        if not email:
            return {'error': 'Email is necessary'}, 400

        user = Users.query.filter_by(email=email).first()
        if not user:
            return {'error': 'Inexistent user'}, 400

        db.session.delete(user)
        db.session.commit()
        return 'OK', 200

    
api.add_resource(UserAPI, '/users')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
