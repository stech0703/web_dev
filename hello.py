from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name=StringField('What is your name ?',validators=[DataRequired()])
    submit=SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY']='hard to guess'







bootstrap=Bootstrap(app)
@app.route('/',methods=['Get','POST'])
def index():
    name= None
    form= NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
    return render_template('index.html',form=form,name=name)

@app.route('/user/<name>')
def user(name):
    l=[]
    for i in range(10):
        l.append(i)
    var = {
         'name':name,
         'list':l
    }    
    return render_template('user.html',context=var)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500    