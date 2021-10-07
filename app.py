from flask import Flask
from flask import render_template
from flask import redirect
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import AnyOf, InputRequired, Length, Email, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = "gva\"Yf124.pi'iFb@j6Pn^:FpA*m`)"

class login_form(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='El usuario es requerido'), Length(min=5, max=10, message='El usuario debe tener entre 5 y 10 caracteres')])
    password = PasswordField('password', validators=[InputRequired('Contraseña es requerida'), AnyOf(values=['superadmin'])])

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/login", methods=['GET','POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        if(form.username.data == 'superadmin' and form.password.data == 'superadmin'):
            return redirect(url_for('admin_dashboard'))
    return render_template('login.html', form=form)

class register_form(FlaskForm):
    nombrecompleto = StringField('nombre', validators=[InputRequired(message='El nombre es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    username = StringField('username', validators=[InputRequired(message='El usuario es requerido'), Length(min=5, max=10, message='El usuario debe tener entre 5 y 10 caracteres')])
    correoelectronico = StringField('correoelectronico', validators=[InputRequired(message='El email es requerido'), Length(min=5, max=10, message='El email debe tener entre 5 y 50 caracteres'), Email(message='Debe ingresar un email valido')])
    password = PasswordField('password', validators=[InputRequired('Contraseña es requerida'), EqualTo('password_repeat', message='Las claves deben coincidir')])
    password_repeat = PasswordField('password_repeat',validators=[InputRequired(message='Repite la clave')])
    tipodocumento = StringField('tipodocumento',validators=[InputRequired(message='Selecciona un tipo de documento')])
    numdocumento = StringField('numdocumento', validators=[InputRequired(message='El número de documento es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])

@app.route("/register", methods=['GET','POST'])
def register():
    form = register_form()
    if form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/admin/dashboard", methods=['GET'])
def admin_dashboard():
    return render_template('admin_dashboard.html')



if __name__ == '__main__':
    app.run(debug=True)
