from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_cors import CORS
from dataclasses import dataclass

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kgkltd.tk@gmail.com'
app.config['MAIL_PASSWORD'] = 'elzsxwurxjajxryn'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)
db = SQLAlchemy(app)
cors = CORS(app)

@dataclass
class ContactResponses(db.Model):
    id:int
    name:str
    email:str
    message:str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    message = db.Column(db.String(1000))

@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=="POST":
        form_name = request.form.get("name")
        form_email = request.form.get("email")
        form_message = request.form.get("message")
        form_data = ContactResponses(name=form_name,email=form_email,message=form_message)
        alert_email = Message(
            subject = "New form response from Portfolio",
            sender = ("Ganesh Kalyan Kommisetti", "kgkltd.tk@gmail.com"),
            recipients = ["srikgk333@gmail.com"],
            body = f"Name: {form_name}\nEmail: {form_email}\nMessage: {form_message}\n"
        )
        mail.send(alert_email)
        db.session.add(form_data)
        db.session.commit()
        status = "success"
        message = "Message sent successfully!"
    else:
        status = "error"
        message = "Method not allowed!"
    response = {
        "status": status,
        "message": message
    }
    return jsonify(response)

@app.route("/contact_responses",methods=["GET"])
def contact_responses():
    if request.args.get("code") == "Kalyan8976":
        responses = ContactResponses.query.all()
    else:
        return {
            "status":"error",
            "message":"Unauthorized access!"
        }
    return jsonify(responses)

if __name__ == '__main__':
    app.run()
