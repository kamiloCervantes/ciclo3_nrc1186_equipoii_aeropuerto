from flask import Flask
from flask import render_template
from flask import redirect
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import AnyOf, InputRequired, Length, Email, EqualTo, NumberRange
import sqlite3
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = "gva\"Yf124.pi'iFb@j6Pn^:FpA*m`)"

def connection():
    con = sqlite3.connect("myflight.sqlite")
    return con

global usuarios
usuarios = [ 
{
    "username" : "superadmin",
    "passwd" : "superadmin",
    "name" : "Super Admin",
    "email" : "root@myflight.com",
    "tipodoc" : 1,
    "numdoc" : 12345
},
{
    "username" : "piloto1",
    "passwd" : "piloto1",
    "name" : "Piloto 1",
    "email" : "piloto1@myflight.com",
    "tipodoc" : 1,
    "numdoc" : 12345
}, 
{
    "username" : "cliente1",
    "passwd" : "cliente1",
    "name" : "Cliente 1",
    "email" : "cliente1@myflight.com",
    "tipodoc" : 1,
    "numdoc" : 12345
}];

class login_form(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='El usuario es requerido'), Length(min=5, max=10, message='El usuario debe tener entre 5 y 10 caracteres')])
    password = PasswordField('password', validators=[InputRequired('Contraseña es requerida')])

@app.route("/")
@app.route("/home")
def home():
    return redirect(url_for('login'))


@app.route("/login", methods=['GET','POST'])
def login():
    form = login_form()    
    if form.validate_on_submit():
        con = connection()
        cur = con.cursor()
        hash_func = hashlib.sha256()
        encoded_pwd = form.password.data.encode()
        hash_func.update(encoded_pwd)
        login_statement = "SELECT * FROM usuarios where username=? and password= ? and activo=1"
        cur.execute(login_statement, [form.username.data, hash_func.hexdigest()])
        usuario = cur.fetchone()
        cur.close()
        if(usuario):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('login'))     
    return render_template('login.html', form=form)

class register_form(FlaskForm):
    nombrecompleto = StringField('nombre', validators=[InputRequired(message='El nombre es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    username = StringField('username', validators=[InputRequired(message='El usuario es requerido'), Length(min=5, max=50, message='El usuario debe tener entre 5 y 10 caracteres')])
    correoelectronico = StringField('correoelectronico', validators=[InputRequired(message='El email es requerido'), Length(min=5, max=50, message='El email debe tener entre 5 y 50 caracteres'), Email(message='Debe ingresar un email valido')])
    password = PasswordField('password', validators=[InputRequired('Contraseña es requerida'), EqualTo('password_repeat', message='Las claves deben coincidir')])
    password_repeat = PasswordField('password_repeat',validators=[InputRequired(message='Repite la clave')])
    tipodocumento = StringField('tipodocumento',validators=[InputRequired(message='Selecciona un tipo de documento')])
    numdocumento = StringField('numdocumento', validators=[InputRequired(message='El número de documento es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])

@app.route("/register", methods=['GET','POST'])
def register():
    form = register_form()
    con = connection()
    cur = con.cursor()
    if form.validate_on_submit():
        persona_statement = "INSERT INTO personas (nombres,apellidos,fecha_nacimiento,num_documento,nro_celular,opciones_tipo_documento_id) VALUES (?,'','',?,'',?)"
        cur.execute(persona_statement, [form.nombrecompleto.data, form.numdocumento.data, form.tipodocumento.data])
        personas_id = cur.lastrowid
        hash_func = hashlib.sha256()
        encoded_pwd = form.password.data.encode()
        hash_func.update(encoded_pwd)
        usuario_statement = "INSERT INTO usuarios (username, password, activo, personas_id)  VALUES (?,?,?,?)"
        cur.execute(usuario_statement, [form.username.data, hash_func.hexdigest(), '1', personas_id])
        usuarios_id = cur.lastrowid
        roles_statement = "INSERT INTO usuarios_has_roles (usuarios_id,roles_id) VALUES (?,?)"
        cur.execute(roles_statement, [usuarios_id, 3])
        cur.close()
        con.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/admin/dashboard", methods=['GET'])
def admin_dashboard():
    return render_template('admin_dashboard.html')


class flights_add_form(FlaskForm):
    codigovuelo = StringField(u'Código de vuelo', validators=[InputRequired(message='El código de vuelo es requerido'), Length(min=5, max=50, message='El código de vuelo debe tener entre 5 y 50 caracteres')])
    aeronave = SelectField(u'Aeronave', choices=[('1', 'Aeronave 1'), ('2', 'Aeronave 2'), ('3', 'Aeronave 3')])
    piloto = SelectField(u'Piloto', choices=[('1', 'Piloto 1'), ('2', 'Piloto 2'), ('3', 'Piloto 3')])
    capacidad = StringField(u'Capacidad', validators=[InputRequired(message='Ingrese la capacidad de personas para este vuelo'), NumberRange(min=0, max=1000, message='La capacidad no puede ser mayor que %(max)s')])
    piloto = SelectField(u'Ruta', choices=[('1', 'Ruta 1'), ('2', 'Ruta 2'), ('3', 'Ruta 3')])

   
@app.route("/admin/flights/add", methods=['GET','POST'])
def flights_add():
    form = flights_add_form()
    if form.validate_on_submit():
        return redirect(url_for('admin_dashboard'))
    return render_template('flights_add.html', form=form)

class planes_add_form(FlaskForm):
    codigoaeronave = StringField(u'Código de aeronave', validators=[InputRequired(message='El código de aeronave es requerido'), Length(min=5, max=50, message='El código de aeronave debe tener entre 5 y 50 caracteres')])
    marca = StringField(u'Marca', validators=[InputRequired(message='La marca de la aeronave es requerida'), Length(min=2, max=50, message='La marca de aeronave debe tener entre 2 y 50 caracteres')])
    modelo = StringField(u'Modelo', validators=[InputRequired(message='El modelo de la aeronave es requerido'), Length(min=5, max=50, message='El modelo de la aeronave debe tener entre 5 y 50 caracteres')])
    capacidad = StringField(u'Capacidad', validators=[InputRequired(message='La capacidad de la aeronave es requerido'), NumberRange(min=0, max=1000, message='La capacidad no puede ser mayor que %(max)s')])
    estado = SelectField(u'Estado', choices=[('1', 'Activo'), ('2', 'En reparación'), ('3', 'Inactivo')])
  
   

@app.route("/admin/planes/add", methods=['GET','POST'])
def planes_add():
    form = planes_add_form()
    if form.validate_on_submit():
        return redirect(url_for('admin_dashboard'))
    return render_template('planes_add.html', form=form)

class routes_add_form(FlaskForm):
    codigoruta = StringField(u'Código de ruta', validators=[InputRequired(message='El código de ruta es requerido'), Length(min=5, max=50, message='El código de ruta debe tener entre 5 y 50 caracteres')])
    destino = StringField(u'Nombre del destino', validators=[InputRequired(message='El nombre del destino es requerido'), Length(min=5, max=50, message='El nombre del destino debe tener entre 5 y 50 caracteres')])
    destinopadre = SelectField(u'Destino padre', choices=[('0', 'Ninguno'), ('1', 'Destino 1'), ('2', 'Destino 2')])
  
   

@app.route("/admin/routes/add", methods=['GET','POST'])
def routes_add():
    form = routes_add_form()
    if form.validate_on_submit():
        return redirect(url_for('admin_dashboard'))
    return render_template('routes_add.html', form=form)


class locations_add_form(FlaskForm):
    pais = SelectField(u'Pais', choices=[('1', 'Colombia'), ('1', 'México'), ('2', 'Venezuela')])
    departamento = SelectField(u'Departamento', choices=[('1', 'Córdoba'), ('1', 'Antioquia'), ('2', 'Cundinamarca')])
    ciudad = SelectField(u'Ciudad', choices=[('1', 'Montería'), ('1', 'Cereté'), ('2', 'Ciénaga de Oro')])
  
   

@app.route("/admin/locations/add", methods=['GET','POST'])
def locations_add():
    form = locations_add_form()
    if form.validate_on_submit():
        return redirect(url_for('admin_dashboard'))
    return render_template('locations_add.html', form=form)


class users_add_form(FlaskForm):
    nombrecompleto = StringField('nombre', validators=[InputRequired(message='El nombre es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    tipodocumento = SelectField(u'Tipo de documento', choices=[('C.C.', 'C.C.'), ('C.E.', 'C.E.'), ('T.I.', 'T.I.')], validate_choice=False)
    numdocumento = StringField('numdocumento', validators=[InputRequired(message='El número de documento es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    correoelectronico = StringField('correoelectronico', validators=[InputRequired(message='El email es requerido'), Length(min=5, max=10, message='El email debe tener entre 5 y 50 caracteres'), Email(message='Debe ingresar un email valido')])
    username = StringField('username', validators=[InputRequired(message='El usuario es requerido'), Length(min=5, max=10, message='El usuario debe tener entre 5 y 10 caracteres')])
    password = PasswordField('password', validators=[InputRequired('Contraseña es requerida'), EqualTo('password_repeat', message='Las claves deben coincidir')])

class users_edit_form(FlaskForm):
    nombrecompleto = StringField('nombre', validators=[InputRequired(message='El nombre es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    tipodocumento = SelectField(u'Tipo de documento', choices=[('C.C.', 'C.C.'), ('C.E.', 'C.E.'), ('T.I.', 'T.I.')], validate_choice=False)
    numdocumento = StringField('numdocumento', validators=[InputRequired(message='El número de documento es requerido')])
    correoelectronico = StringField('correoelectronico', validators=[InputRequired(message='El email es requerido'), Length(min=5, max=50, message='El email debe tener entre 5 y 50 caracteres'), Email(message='Debe ingresar un email valido')])


@app.route("/admin/users/add", methods=['GET','POST'])
def users_add():
    form = users_add_form()
    if form.validate_on_submit():
        return redirect(url_for('admin_dashboard'))
    return render_template('users_add.html', form=form)
    


@app.route("/admin/users/edit/<username>", methods=['GET','POST'])
def users_edit(username):
    form = users_edit_form()
    idx = 0
    for index, user in enumerate(usuarios):
        if(user['username'] == username):
            idx = index
            form.nombrecompleto.data = user['name']
            form.tipodocumento.data = user['tipodoc']
            form.numdocumento.data = user['numdoc']
            form.correoelectronico.data = user['email']
    
    if form.validate_on_submit():
        print(idx)
        updated_user = {
            'name' : form.nombrecompleto.data,
            'tipodoc' : form.tipodocumento.data,
            'numdoc' : form.numdocumento.data,
            'email': form.correoelectronico.data,
            'username' : usuarios[idx]['username'],
            'passwd': usuarios[idx]['passwd']
        }
        
        usuarios[idx] = updated_user
        return redirect(url_for('users_list'))
    return render_template('users_edit.html', form=form, username=username)

@app.route("/admin/users", methods=['GET'])
def users_list():
    return render_template('users_list.html', usuarios=usuarios)


class pilots_add_form(FlaskForm):
    nombrecompleto = StringField('nombre', validators=[InputRequired(message='El nombre es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    tipodocumento = SelectField(u'Tipo de documento', choices=[('1', 'C.C.'), ('2', 'C.E.'), ('3', 'T.I.')])
    numdocumento = StringField('numdocumento', validators=[InputRequired(message='El número de documento es requerido')])
    correoelectronico = StringField('correoelectronico', validators=[InputRequired(message='El email es requerido'), Length(min=5, max=10, message='El email debe tener entre 5 y 50 caracteres'), Email(message='Debe ingresar un email valido')])
    username = StringField('username', validators=[InputRequired(message='El usuario es requerido'), Length(min=5, max=10, message='El usuario debe tener entre 5 y 10 caracteres')])
    password = PasswordField('password', validators=[InputRequired('Contraseña es requerida'), EqualTo('password_repeat', message='Las claves deben coincidir')])
    estado = SelectField(u'Estado', choices=[('1', 'Activo'), ('1', 'En vacaciones'), ('2', 'Incapacitado')])

   

@app.route("/admin/pilots/add", methods=['GET','POST'])
def pilots_add():
    form = pilots_add_form()
    if form.validate_on_submit():
        return redirect(url_for('admin_dashboard'))
    return render_template('pilots_add.html', form=form)


@app.route("/logout")
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)