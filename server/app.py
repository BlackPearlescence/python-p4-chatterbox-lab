from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods=["GET","POST"])
def messages():
    if request.method == "GET":
        messages = []
        for message in Message.query.all():
            messages.append(message.to_dict())
        
        response = make_response(
            jsonify(messages),
            200
        )
        return response
    elif request.method == "POST":
        new_message = Message(
            body=request.json["body"],
            username=request.json["username"],
            # created_at=request.json["created_at"],
        )

        db.session.add(new_message)
        db.session.commit()

        new_message = new_message.to_dict()

        response = make_response(
            jsonify(new_message),
            201
        )

        return response

@app.route('/messages/<int:id>',methods=["GET","PATCH","DELETE"])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == "GET":
        message = message.to_dict()

        response = make_response(
            jsonify(message),
            200
        )
        return response
    elif request.method == "PATCH":
        for attr in request.json:
            setattr(message,attr,request.json[attr])
    
        db.session.add(message)
        db.session.commit()

        message = message.to_dict()

        response = make_response(
            jsonify(message),
            200
        )

        return response
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }

        response = make_response(
            jsonify(response_body),
            200
        )

        return response

if __name__ == '__main__':
    app.run(port=5555)
