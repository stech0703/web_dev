import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash, session,request
from flask_wtf import FlaskForm
from sqlalchemy.orm import query
from wtforms import StringField,TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired
from wtforms import Form
from flask_mail import Mail, Message


app = Flask(__name__)
db = SQLAlchemy(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'warmachinerox'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SUBJECT_PREFIX'] = '[QUERY]'
app.config['FLASK_MAIL_SENDER'] = 'ADMIN <s.tech0703@gmail.com>'
app.config['ADMIN'] = os.environ.get('ADMIN')


mail = Mail(app)



def send_mail(to,subject,template,**kwargs):
    msg=Message(app.config['MAIL_SUBJECT_PREFIX']+subject,sender=app.config['MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)    
    


class Query(db.Model):
    __tablename__='contacts'
    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    subj = db.Column(db.String(100))
    message = db.Column(db.String(200))

    def __repr__(self):
        return f"Query('{self.name}' , '{self.email}' , '{self.subj}' , '{self.message}')"
        
        

@app.route('/',methods=['GET' , 'POST'])
def index():
    if request.method == "POST":
        Name = request.form.get("name")
        Email = request.form.get("email")
        Subj = request.form.get("subj")
        Message = request.form.get("message")
        msgg=Query(name=Name, email=Email, subj=Subj, message=Message)
        db.session.add(msgg)
        db.session.commit()
        if app.config['ADMIN']:
            send_mail(app.config['ADMIN'],'New Query','mail/query',name=Name,email=Email,subj=Subj,message=Message)
        flash('Query submitted successfully... wait for reply from admin!!',category='alert')
        return redirect(url_for('index'))
    return render_template("contact.html")


@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html') , 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html') , 500

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Query=Query)