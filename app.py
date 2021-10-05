from flask import Flask
from flask import render_template
from flask import redirect
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import AnyOf, InputRequired, Length

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


@app.route("/admin/dashboard", methods=['GET'])
def admin_dashboard():
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
