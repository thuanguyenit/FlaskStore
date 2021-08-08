from flask_wtf import FlaskForm
from wtforms.fields import core
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
import wtforms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class SignUpForm(FlaskForm):
    inputFullName = wtforms.StringField('Full name', [DataRequired(message='Please enter your full name!')])
    inputEmail = wtforms.StringField('Email address', [Email(message='Not availed email address!'),
                                                       DataRequired(message='Please enter your email!!')])
        
    inputPhone = wtforms.StringField('Full name', [DataRequired(message='Please enter your phone number!')])
    inputAddress = wtforms.StringField('Full name', [DataRequired(message='Please enter your adrress!')])
                                                       
    inputPassword = wtforms.PasswordField('Password', [DataRequired(message='Enter your pass word!'),
                                                       EqualTo('inputConfirmPassword',
                                                               message="Password does not match")])
    inputConfirmPassword = wtforms.PasswordField('Confirm Password')
    submit = wtforms.SubmitField('Sign Up')


class SignInForm(FlaskForm):
    inputEmail = wtforms.StringField('Email address', [Email(message='Not availed email address!'), DataRequired(message='Please enter your email!!')], )
    inputPassword = wtforms.PasswordField('Password', [DataRequired(message='Enter your pass word!')])
    submit = wtforms.SubmitField('Sign In')

class AddProductForm(FlaskForm):    
    inputName = wtforms.StringField('Product name', [DataRequired(message='Please enter your product name!')])
    inputDes = wtforms.TextAreaField('Product des', [DataRequired(message='Please enter your product description!')])
    inputPrice = wtforms.IntegerField('Product name', [DataRequired(message='Please enter your product Price!')])
    submit = wtforms.SubmitField("Add")
    
class EditProductForm(FlaskForm):
    inputName = wtforms.StringField('Product name', [DataRequired(message='Please enter your product name!')])
    inputDes = wtforms.StringField('Product des', [DataRequired(message='Please enter your product description!')])
    inputPrice = wtforms.IntegerField('Product name', [DataRequired(message='Please enter your product Price!')])
    inputStatus = wtforms.SelectField(coerce=int)
    submit = wtforms.SubmitField("Save")

class OrderForm(FlaskForm):
    inputAddress = wtforms.SelectField(coerce=int)
    inputPhone = wtforms.SelectField(coerce=int)
    submit = wtforms.SubmitField("Save")
