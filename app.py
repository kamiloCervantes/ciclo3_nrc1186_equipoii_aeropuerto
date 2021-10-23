from flask import Flask, g
from flask import render_template
from flask import redirect
from flask import session
from flask import request
from flask import jsonify
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField
from wtforms.validators import AnyOf, InputRequired, Length, Email, EqualTo, NumberRange
import sqlite3
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = "gva\"Yf124.pi'iFb@j6Pn^:FpA*m`)"

def connection():
    con = sqlite3.connect("myflight.sqlite")
    return con

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
        login_statement = "SELECT usuarios.id, roles.id, roles.nombre_rol FROM usuarios inner join usuarios_has_roles as uhr on uhr.usuarios_id = usuarios.id inner join roles on uhr.roles_id = roles.id where usuarios.username=? and usuarios.password= ? and usuarios.activo=1 "
        cur.execute(login_statement, [form.username.data, hash_func.hexdigest()])
        usuario = cur.fetchall()
        cur.close()
        if len(usuario) == 1:
            print(usuario)
            session['user_id'] = usuario[0][0]
            session['rol_id'] = usuario[0][1]
            session['rol_nombre'] = usuario[0][2]

            if usuario[0][2] == 'root':
                return redirect(url_for('admin_dashboard'))
            elif usuario[0][2] == 'piloto':
                return redirect(url_for('pilot_dashboard'))
            elif usuario[0][2] == 'cliente':
                return redirect(url_for('client_flights'))
            else:
                return redirect(url_for('login'))
        elif len(usuario) > 1:
            session['user_id'] = usuario[0][0]
            return redirect(url_for('roles_selector'))
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
        usuario_statement = "INSERT INTO usuarios (username, password, activo, personas_id, email)  VALUES (?,?,?,?,?)"
        cur.execute(usuario_statement, [form.username.data, hash_func.hexdigest(), '1', personas_id, form.correoelectronico.data])
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


class locations_form(FlaskForm):
    nombreaeropuerto = StringField(u'Nombre del aeropuerto', validators=[InputRequired(message='El nombre del aeropuerto es requerido'), Length(min=5, max=255, message='El nombre del aeropuerto debe tener entre 5 y 255 caracteres')])
    siglaaeropuerto = StringField(u'Sigla del aeropuerto', validators=[InputRequired(message='La sigla del aeropuerto es requerida'), Length(min=3, max=5, message='El nombre del aeropuerto debe tener entre 3 y 5 caracteres')])
    pais = SelectField(u'Pais', coerce=int, validate_choice=False)
    departamento = SelectField(u'Departamento', coerce=int, validate_choice=False)
    ciudad = SelectField(u'Ciudad', coerce=int, validate_choice=False)
  
   

@app.route("/admin/locations/add", methods=['GET','POST'])
def locations_add():
    form = locations_form()
    con = connection()
    cur = con.cursor()
    #choice queries
    paises_choice_statement = "SELECT id, nombre from paises"
    cur.execute(paises_choice_statement)
    paises_list = cur.fetchall()
    departamentos_choice_statement = "SELECT id, nombre from departamentos"
    cur.execute(departamentos_choice_statement)
    departamentos_list = cur.fetchall()
    municipios_choice_statement = "SELECT id, nombre from municipios"
    cur.execute(municipios_choice_statement)
    municipios_list = cur.fetchall()
    #setting choices
    form.pais.choices = paises_list
    form.departamento.choices = departamentos_list
    form.ciudad.choices = municipios_list
    if form.validate_on_submit():
        try:
            destinos_statement = "INSERT INTO destinos (nombre_aeropuerto,sigla_aeropuerto,municipios_id) VALUES (?,?,?)"
            cur.execute(destinos_statement, [form.nombreaeropuerto.data, form.siglaaeropuerto.data, form.ciudad.data])
        except:
            return redirect(url_for('locations_add', error_message="No se pudo guardar el registro en la BD"))
        else:
            con.commit()
            cur.close()
            return redirect(url_for('locations_list'))
    return render_template('locations_add.html', form=form)

@app.route("/admin/locations", methods=['GET','POST','PUT','DELETE'])
def admin_locations_rest_resource():
    if request.method == 'DELETE':
        con = connection()
        cur = con.cursor()        
        location_id = request.form['location_id']
        location_statement = "delete from destinos where id=?"
        try:
            cur.execute(location_statement, [location_id])
                       
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo eliminar el registro'}]),501
        else:
             #con.commit()           
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue eliminado'}])
        


@app.route("/admin/locations/list", methods=['GET'])
def locations_list():
    con = connection()
    cur = con.cursor()
    locations_statement = "SELECT destinos.id, destinos.nombre_aeropuerto, destinos.sigla_aeropuerto, municipios.nombre, departamentos.nombre, paises.nombre from destinos inner join municipios on municipios.id = destinos.municipios_id inner join departamentos on departamentos.id = municipios.departamentos_id inner join paises on paises.id = departamentos.paises_id order by destinos.id asc limit 10"
    cur.execute(locations_statement)
    locations = cur.fetchall()
    return render_template('locations_list.html', locations=locations)

@app.route("/admin/locations/edit/<location_id>", methods=['GET', 'POST'])
def locations_edit(location_id):
    form = locations_form()
    con = connection()
    cur = con.cursor()
    #choice queries
    paises_choice_statement = "SELECT id, nombre from paises"
    cur.execute(paises_choice_statement)
    paises_list = cur.fetchall()
    departamentos_choice_statement = "SELECT id, nombre from departamentos"
    cur.execute(departamentos_choice_statement)
    departamentos_list = cur.fetchall()
    municipios_choice_statement = "SELECT id, nombre from municipios"
    cur.execute(municipios_choice_statement)
    municipios_list = cur.fetchall()
    #loading data
    location_statement = "SELECT destinos.id, destinos.nombre_aeropuerto, destinos.sigla_aeropuerto, municipios.id, departamentos.id, paises.id from destinos inner join municipios on municipios.id = destinos.municipios_id inner join departamentos on departamentos.id = municipios.departamentos_id inner join paises on paises.id = departamentos.paises_id where destinos.id=?"
    cur.execute(location_statement, location_id)
    location = cur.fetchone()
    #setting choices
    form.pais.choices = paises_list
    form.departamento.choices = departamentos_list
    form.ciudad.choices = municipios_list
    if not location:
        return redirect(url_for('locations_list'))
    else:
        form.nombreaeropuerto.data = location[1]
        form.siglaaeropuerto.data = location[2]
        form.ciudad.data = location[3]
        form.departamento.data = location[4]
        form.pais.data = location[5]    
    if form.validate_on_submit():
        try:
            nombreaeropuerto = location[1] if location[1] == request.form['nombreaeropuerto'] else request.form['nombreaeropuerto']
            siglaaeropuerto = location[2] if location[2] == request.form['siglaaeropuerto'] else request.form['siglaaeropuerto'] 
            ciudad = location[3] if location[3] == request.form['ciudad'] else request.form['ciudad'] 
            print(nombreaeropuerto)
            print(form.nombreaeropuerto.data)
            print(request.form['nombreaeropuerto'])
            destinos_statement = "UPDATE destinos SET nombre_aeropuerto = ?, sigla_aeropuerto = ?, municipios_id = ? WHERE id = ?"
            cur.execute(destinos_statement, [nombreaeropuerto, siglaaeropuerto, ciudad, location_id])
        except:
            return redirect(url_for('locations_edit', location_id=location_id, error_message="No se pudo actualizar el registro en la BD"))
        else:
            con.commit()
            cur.close()
            return redirect(url_for('locations_list'))    
    
    return render_template('locations_edit.html', form=form, location_id=location_id)

  
    

class users_form(FlaskForm):
    nombres = StringField('Nombres', validators=[InputRequired(message='El nombre es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    apellidos = StringField('Apellidos', validators=[InputRequired(message='El apellido es requerido'), Length(min=5, max=50, message='El apellido debe tener entre 5 y 50 caracteres')])
    tipodocumento = SelectField(u'Tipo de documento', coerce=int, validate_choice=False)
    numdocumento = StringField('Documento de identidad', validators=[InputRequired(message='El número de documento es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    fechanacimiento = DateField('Fecha de nacimiento')
    correoelectronico = StringField('Email', validators=[InputRequired(message='El email es requerido'), Length(min=5, max=50, message='El email debe tener entre 5 y 50 caracteres'), Email(message='Debe ingresar un email valido')])
    nrocelular = StringField('Celular', validators=[Length(min=10, max=10, message='El celular debe tener 10 caracteres')])
    username = StringField('username', validators=[InputRequired(message='El usuario es requerido'), Length(min=5, max=40, message='El usuario debe tener entre 5 y 10 caracteres')])
    password = PasswordField('password', validators=[InputRequired('Contraseña es requerida')])
    rol = SelectField(u'Rol', coerce=int, validate_choice=False)

class users_form_edit(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='El usuario es requerido'), Length(min=5, max=40, message='El usuario debe tener entre 5 y 10 caracteres')])
    # nombres = StringField('Nombres', validators=[InputRequired(message='El nombre es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    # apellidos = StringField('Apellidos', validators=[InputRequired(message='El apellido es requerido'), Length(min=5, max=50, message='El apellido debe tener entre 5 y 50 caracteres')])
    # tipodocumento = SelectField(u'Tipo de documento', coerce=int, validate_choice=False)
    # numdocumento = StringField('Documento de identidad', validators=[InputRequired(message='El número de documento es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    # fechanacimiento = DateField('Fecha de nacimiento')
    # correoelectronico = StringField('Email', validators=[InputRequired(message='El email es requerido'), Length(min=5, max=50, message='El email debe tener entre 5 y 50 caracteres'), Email(message='Debe ingresar un email valido')])
    # nrocelular = StringField('Celular', validators=[Length(min=10, max=10, message='El celular debe tener 10 caracteres')])
    # password = PasswordField('password', validators=[])
    # rol = SelectField(u'Rol', coerce=int, validate_choice=False)

@app.route("/admin/users/add", methods=['GET','POST'])
def users_add():
    form = users_form()
    con = connection()
    cur = con.cursor()
    tipodoc_statement = "SELECT id,tipo_documento_opcion FROM opciones_tipo_documento where visible=1"
    cur.execute(tipodoc_statement)
    tipodocumento_list = cur.fetchall()
    form.tipodocumento.choices = tipodocumento_list
    rol_statement = "SELECT roles.id, roles.nombre_rol FROM roles"
    cur.execute(rol_statement)
    roles_list = cur.fetchall()
    form.rol.choices = roles_list
    if form.validate_on_submit():
        persona_statement = "INSERT INTO personas (nombres,apellidos,fecha_nacimiento,num_documento,nro_celular,opciones_tipo_documento_id) VALUES (?,?,?,?,?,?)"
        cur.execute(persona_statement, [form.nombres.data, form.apellidos.data, form.fechanacimiento.data, form.numdocumento.data, form.nrocelular.data, form.tipodocumento.data])
        personas_id = cur.lastrowid
        hash_func = hashlib.sha256()
        encoded_pwd = form.password.data.encode()
        hash_func.update(encoded_pwd)
        usuario_statement = "INSERT INTO usuarios (username, password, activo, personas_id, email)  VALUES (?,?,?,?,?)"
        cur.execute(usuario_statement, [form.username.data, hash_func.hexdigest(), '1', personas_id, form.correoelectronico.data])
        usuarios_id = cur.lastrowid
        roles_statement = "INSERT INTO usuarios_has_roles (usuarios_id,roles_id) VALUES (?,?)"
        cur.execute(roles_statement, [usuarios_id, form.rol.data])
        cur.close()
        con.commit()
        return redirect(url_for('users_list'))
    return render_template('users_add.html', form=form)
    


@app.route("/admin/users/edit/<user_id>", methods=['GET','POST'])
def users_edit(user_id):
    form = users_form_edit()
    con = connection()
    cur = con.cursor()
    user_statement = "SELECT usuarios.id, usuarios.username, usuarios.password, usuarios.email FROM usuarios where usuarios.id=?"
    cur.execute(user_statement, [user_id])
    user = cur.fetchone()
    if not user:
        return redirect(url_for('users_list'))
    else:
        form.username.data = user[1]  
    print(form.validate_on_submit())
    if form.validate_on_submit():
        username = user[1] if user[1] == request.form['username'] else request.form['username']
        usuario_statement = "UPDATE usuarios SET username = ?,  activo = ? WHERE id = ? "
        cur.execute(usuario_statement, [username, '1', user[0]])      
        cur.close()
        con.commit()
        return redirect(url_for('users_list'))
    return render_template('users_edit.html', form=form, user_id=user_id)

@app.route("/admin/users/list", methods=['GET'])
def users_list():
    con = connection()
    cur = con.cursor()
    users_statement = "SELECT usuarios.id, usuarios.username, group_concat(roles.nombre_rol) from usuarios inner join usuarios_has_roles on usuarios.id = usuarios_has_roles.usuarios_id inner join roles on roles.id = usuarios_has_roles.roles_id group by usuarios.id order by usuarios.id asc limit 10"
    cur.execute(users_statement)
    users = cur.fetchall()
    return render_template('users_list.html', users=users)

@app.route("/admin/users", methods=['GET','POST','PUT','DELETE'])
def admin_users_rest_resource():
    if request.method == 'DELETE':
        con = connection()
        cur = con.cursor()        
        user_id = request.form['user_id']
        user_statement = "delete from usuarios where id=?"
        try:
            cur.execute(user_statement, [user_id])
                       
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo eliminar el registro'}]),501
        else:
             #con.commit()           
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue eliminado'}])


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
    session.clear()
    return redirect(url_for('login'))


@app.before_request
def check_session():
    user_id = session.get('user_id')
    role_id = session.get('rol_id')
    exceptions = ['/login', '/register', '/logout', '/auth/roles/selector', '/home', '/','/auth/forbidden']
    if request.path.find('static') > 0 or request.path.find('favicon') > 0 or request.path in exceptions or request.method != 'GET':
        pass
    else:
        con = connection()
        cur = con.cursor()
        path = request.path
        acl_statement = "SELECT distinct recursos.ruta_relativa FROM usuarios inner join usuarios_has_roles as uhr on uhr.usuarios_id = usuarios.id inner join roles on uhr.roles_id = roles.id inner join roles_acceso_recursos as rar on rar.roles_id = roles.id inner join recursos on rar.recursos_id = recursos.id where usuarios.id=? and usuarios.activo=1 and INSTR(?, recursos.ruta_relativa)"
        cur.execute(acl_statement, [user_id, path])
        acl = cur.fetchone()
        cur.close()
        if not acl:
            return redirect(url_for('auth_forbidden'))

@app.route("/admin/routes")
def routes_list():
    return render_template("routes_list.html")


@app.route("/auth/roles/selector", methods=['GET','POST'])
def roles_selector():
    con = connection()
    cur = con.cursor()
    if request.method == 'GET':
        user_id = session.get('user_id')
        roles_statement = "SELECT roles.id, roles.nombre_rol FROM usuarios inner join usuarios_has_roles as uhr on uhr.usuarios_id = usuarios.id inner join roles on uhr.roles_id = roles.id where usuarios.id=? and usuarios.activo=1 "
        cur.execute(roles_statement, [user_id])
        roles = cur.fetchall()
        cur.close()
        con.commit()
        return render_template("roles_selector.html", roles=roles)
    elif request.method == 'POST':
        selected_rol = request.form['rol']
        rol_statement = "SELECT roles.id, roles.nombre_rol FROM roles where roles.id=?"
        cur.execute(rol_statement, [selected_rol])
        rol = cur.fetchone()
        if rol:
            session['rol_id'] = rol[0]
            session['rol_nombre'] = rol[1]
            role = rol[1]
            if role == 'root':
                return redirect(url_for('admin_dashboard'))
            elif role == 'piloto':
                return redirect(url_for('pilot_dashboard'))
            elif role == 'cliente':
                return redirect(url_for('client_flights'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))


@app.route("/auth/forbidden")
def auth_forbidden():
    return render_template("auth_forbidden.html")


class settings_roles_form(FlaskForm):
    nombre_rol = StringField('Nombre del rol', validators=[InputRequired(message='El nombre del rol es requerido'), Length(min=5, max=45, message='El nombre del rol debe tener entre 5 y 45 caracteres')])
    descripcion = StringField('Descripcion', validators=[InputRequired(message='La descripción del rol es requerida'), Length(min=5, max=45, message='El nombre del rol debe tener entre 5 y 45 caracteres')])
    homepage = SelectField(u'Home', coerce=int, validate_choice=False)

class settings_roles_form_edit(FlaskForm):
    nombre_rol_edit = StringField('Nombre del rol', validators=[InputRequired(message='El nombre del rol es requerido'), Length(min=5, max=45, message='El nombre del rol debe tener entre 5 y 45 caracteres')])
    descripcion_edit = StringField('Descripcion', validators=[InputRequired(message='La descripción del rol es requerida'), Length(min=5, max=45, message='El nombre del rol debe tener entre 5 y 45 caracteres')])
    homepage_edit = SelectField(u'Home', coerce=int, validate_choice=False)

class settings_recursos_form(FlaskForm):
    nombre_recurso = StringField('Nombre del recurso', validators=[InputRequired(message='El nombre del recurso es requerido'), Length(min=5, max=45, message='El nombre del recurso debe tener entre 5 y 45 caracteres')])
    descripcion_recurso = StringField('Descripcion', validators=[InputRequired(message='La descripción del recurso es requerida'), Length(min=5, max=255, message='La descripcion del recurso debe tener entre 5 y 255 caracteres')])
    codigo_recurso = StringField(u'Código del recurso', validators=[InputRequired(message='El código del recurso es requerido'), Length(min=5, max=45, message='El código del recurso  debe tener entre 5 y 45 caracteres')])
    ruta_relativa =  StringField('Ruta relativa', validators=[InputRequired(message='La ruta relativa del recurso es requerida'), Length(min=5, max=255, message='La ruta relativa del recurso debe tener entre 5 y 255 caracteres')])

class settings_recursos_form_edit(FlaskForm):
    nombre_recurso_edit = StringField('Nombre del recurso', validators=[InputRequired(message='El nombre del recurso es requerido'), Length(min=5, max=45, message='El nombre del recurso debe tener entre 5 y 45 caracteres')])
    descripcion_recurso_edit = StringField('Descripcion', validators=[InputRequired(message='La descripción del recurso es requerida'), Length(min=5, max=255, message='La descripcion del recurso debe tener entre 5 y 255 caracteres')])
    codigo_recurso_edit = StringField(u'Código del recurso', validators=[InputRequired(message='El código del recurso es requerido'), Length(min=5, max=45, message='El código del recurso  debe tener entre 5 y 45 caracteres')])
    ruta_relativa_edit =  StringField('Ruta relativa', validators=[InputRequired(message='La ruta relativa del recurso es requerida'), Length(min=5, max=255, message='La ruta relativa del recurso debe tener entre 5 y 255 caracteres')])

class settings_paises_form(FlaskForm):
    nombre_pais = StringField('Nombre del pais', validators=[InputRequired(message='El nombre del pais es requerido'), Length(min=5, max=255, message='El nombre del pais debe tener entre 5 y 255 caracteres')])
    descripcion_pais = StringField('Descripcion', validators=[InputRequired(message='La descripción del pais es requerida'), Length(min=5, max=255, message='La descripcion del pais debe tener entre 5 y 255 caracteres')])
   
class settings_paises_form_edit(FlaskForm):
    nombre_pais_edit = StringField('Nombre del pais', validators=[InputRequired(message='El nombre del pais es requerido'), Length(min=5, max=255, message='El nombre del pais debe tener entre 5 y 255 caracteres')])
    descripcion_pais_edit = StringField('Descripcion', validators=[InputRequired(message='La descripción del pais es requerida'), Length(min=5, max=255, message='La descripcion del pais debe tener entre 5 y 255 caracteres')])
   
class settings_departamentos_form(FlaskForm):
    nombre_departamento = StringField('Nombre del departamento', validators=[InputRequired(message='El nombre del departamento es requerido'), Length(min=5, max=255, message='El nombre del departamento debe tener entre 5 y 255 caracteres')])
    descripcion_departamento = StringField('Descripcion', validators=[InputRequired(message='La descripción del departamento es requerida'), Length(min=5, max=255, message='La descripcion del departamento debe tener entre 5 y 255 caracteres')])
    pais_departamento = SelectField(u'País', coerce=int, validate_choice=False)

class settings_departamentos_form_edit(FlaskForm):
    nombre_departamento_edit = StringField('Nombre del departamento', validators=[InputRequired(message='El nombre del departamento es requerido'), Length(min=5, max=255, message='El nombre del departamento debe tener entre 5 y 255 caracteres')])
    descripcion_departamento_edit = StringField('Descripcion', validators=[InputRequired(message='La descripción del departamento es requerida'), Length(min=5, max=255, message='La descripcion del departamento debe tener entre 5 y 255 caracteres')])
    pais_departamento_edit = SelectField(u'País', coerce=int, validate_choice=False)

class settings_municipios_form(FlaskForm):
    nombre_municipio = StringField('Nombre del municipio', validators=[InputRequired(message='El nombre del municipio es requerido'), Length(min=5, max=255, message='El nombre del municipio debe tener entre 5 y 255 caracteres')])
    descripcion_municipio = StringField('Descripcion', validators=[InputRequired(message='La descripción del municipio es requerida'), Length(min=5, max=255, message='La descripcion del municipio debe tener entre 5 y 255 caracteres')])
    departamento_municipio = SelectField(u'Departamento', coerce=int, validate_choice=False)

class settings_municipios_form_edit(FlaskForm):
    nombre_municipio_edit = StringField('Nombre del municipio', validators=[InputRequired(message='El nombre del municipio es requerido'), Length(min=5, max=255, message='El nombre del municipio debe tener entre 5 y 255 caracteres')])
    descripcion_municipio_edit = StringField('Descripcion', validators=[InputRequired(message='La descripción del municipio es requerida'), Length(min=5, max=255, message='La descripcion del municipio debe tener entre 5 y 255 caracteres')])
    departamento_municipio_edit = SelectField(u'Departamento', coerce=int, validate_choice=False)

@app.route("/admin/settings")
def admin_settings():
    con = connection()
    cur = con.cursor()
    #forms
    roles_form = settings_roles_form()
    roles_form_edit = settings_roles_form_edit()
    recursos_form = settings_recursos_form()
    recursos_form_edit = settings_recursos_form_edit()
    paises_form = settings_paises_form()
    paises_form_edit = settings_paises_form_edit()
    departamentos_form = settings_departamentos_form()
    departamentos_form_edit = settings_departamentos_form_edit()
    municipios_form = settings_municipios_form()
    municipios_form_edit = settings_municipios_form_edit()
    #entities
    rol_statement = "SELECT roles.id, roles.nombre_rol, roles.descripcion, recursos.ruta_relativa FROM roles left join recursos on recursos.id = roles.homepage ORDER BY roles.id ASC LIMIT 10"
    cur.execute(rol_statement)
    roles = cur.fetchall()    
    recursos_statement = "select recursos.id, recursos.nombre_recurso, recursos.descripcion, recursos.codigo_recurso, recursos.ruta_relativa from recursos order by id limit 10"
    cur.execute(recursos_statement)
    recursos_list = cur.fetchall() 
    paises_statement = "select paises.id, paises.nombre, paises.descripcion from paises order by id limit 10"
    cur.execute(paises_statement)
    paises_list = cur.fetchall() 
    departamentos_statement = "select departamentos.id, departamentos.nombre, departamentos.descripcion, paises.nombre from departamentos inner join paises on paises.id = departamentos.paises_id order by departamentos.id limit 10"
    cur.execute(departamentos_statement)
    departamentos_list = cur.fetchall() 
    municipios_statement = "select municipios.id, municipios.nombre, municipios.descripcion, departamentos.nombre from municipios inner join departamentos on departamentos.id = municipios.departamentos_id order by municipios.id limit 10"
    cur.execute(municipios_statement)
    municipios_list = cur.fetchall()
    #choices queries
    resources_choices_statement = "select id,ruta_relativa from recursos"
    cur.execute(resources_choices_statement)
    resources_choices_list = cur.fetchall() 
    paises_choice_statement = "select paises.id, paises.nombre from paises order by id"
    cur.execute(paises_choice_statement)
    paises_choices_list = cur.fetchall() 
    departamentos_choice_statement = "select departamentos.id, departamentos.nombre from departamentos order by departamentos.id"
    cur.execute(departamentos_choice_statement)
    departamentos_choices_list = cur.fetchall()
    # setting choices
    roles_form.homepage.choices = resources_choices_list
    roles_form_edit.homepage_edit.choices = resources_choices_list
    departamentos_form.pais_departamento.choices = paises_choices_list
    departamentos_form_edit.pais_departamento_edit.choices = paises_choices_list
    municipios_form.departamento_municipio.choices = departamentos_choices_list
    municipios_form_edit.departamento_municipio_edit.choices = departamentos_choices_list
    
    
    cur.close()
    return render_template("admin_settings.html",
    roles_form=roles_form, 
    roles_form_edit=roles_form_edit, 
    roles_list=roles, 
    recursos_list=recursos_list,
    recursos_form=recursos_form, 
    recursos_form_edit=recursos_form_edit,
    paises_list=paises_list,
    paises_form=paises_form, 
    paises_form_edit=paises_form_edit,
    departamentos_list=departamentos_list,
    departamentos_form=departamentos_form, 
    departamentos_form_edit=departamentos_form_edit,
    municipios_list=municipios_list,
    municipios_form=municipios_form, 
    municipios_form_edit=municipios_form_edit,
    error_message=request.args.get('error_message')
    )  

@app.route("/admin/settings/roles/add", methods=['POST'])
def admin_settings_roles_add():
    form = settings_roles_form() 
    if form.validate_on_submit():
        con = connection()
        cur = con.cursor()
        rol_statement = "INSERT INTO roles (nombre_rol,descripcion,homepage) VALUES (?,?,?)"
        cur.execute(rol_statement, [form.nombre_rol.data, form.descripcion.data, form.homepage.data])
        cur.close()
        con.commit()
        return redirect(url_for('admin_settings'))
    else:
        error_message = ''
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                error_message+= err +';'
        return redirect(url_for('admin_settings', error_message=error_message))
    

@app.route("/admin/settings/recursos/add", methods=['POST'])
def admin_settings_recursos_add():
    form = settings_recursos_form()     
    if form.validate_on_submit():
        con = connection()
        cur = con.cursor()
        recurso_statement = "INSERT INTO recursos (nombre_recurso,descripcion,codigo_recurso,ruta_relativa) VALUES (?,?,?,?)"
        cur.execute(recurso_statement, [form.nombre_recurso.data, form.descripcion_recurso.data, form.codigo_recurso.data, form.ruta_relativa.data])
        cur.close()
        con.commit()
        return redirect(url_for('admin_settings'))
    else:
        error_message = ''
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                error_message+= err +';'
        return redirect(url_for('admin_settings', error_message=error_message))

@app.route("/admin/settings/paises/add", methods=['POST'])
def admin_settings_paises_add():
    form = settings_paises_form()     
    if form.validate_on_submit():
        con = connection()
        cur = con.cursor()
        pais_statement = "INSERT INTO paises (nombre,descripcion) VALUES (?,?)"
        cur.execute(pais_statement, [form.nombre_pais.data, form.descripcion_pais.data])
        cur.close()
        con.commit()
        return redirect(url_for('admin_settings'))
    else:
        error_message = ''
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                error_message+= err +';'
        return redirect(url_for('admin_settings', error_message=error_message))

@app.route("/admin/settings/departamentos/add", methods=['POST'])
def admin_settings_departamentos_add():
    form = settings_departamentos_form()     
    if form.validate_on_submit():
        con = connection()
        cur = con.cursor()
        departamento_statement = "INSERT INTO departamentos (nombre,descripcion,paises_id) VALUES (?,?,?)"
        cur.execute(departamento_statement, [form.nombre_departamento.data, form.descripcion_departamento.data, form.pais_departamento.data])
        cur.close()
        con.commit()
        return redirect(url_for('admin_settings'))
    else:
        error_message = ''
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                error_message+= err +';'
        return redirect(url_for('admin_settings', error_message=error_message))

@app.route("/admin/settings/municipios/add", methods=['POST'])
def admin_settings_municipios_add():
    form = settings_municipios_form()     
    if form.validate_on_submit():
        con = connection()
        cur = con.cursor()
        municipio_statement = "INSERT INTO municipios (nombre,descripcion,departamentos_id) VALUES (?,?,?)"
        cur.execute(municipio_statement, [form.nombre_municipio.data, form.descripcion_municipio.data, form.departamento_municipio.data])
        cur.close()
        con.commit()
        return redirect(url_for('admin_settings'))
    else:
        error_message = ''
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                error_message+= err +';'
        return redirect(url_for('admin_settings', error_message=error_message))
  

@app.route("/admin/settings/roles", methods=['GET','POST','PUT','DELETE'])
def admin_settings_roles_rest_resource():
    if request.method == 'DELETE':
        try:
            con = connection()
            cur = con.cursor()        
            rol_id = request.form['rol_id']
            rol_statement = "delete from roles where id=?"
            cur.execute(rol_statement, [rol_id])       
            #con.commit()                
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo eliminar el registro'}]),501
        else:                      
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue eliminado'}])
    
    elif request.method == 'GET':
        try:
            con = connection()
            cur = con.cursor()    
            rol_id = request.args.get('rol_id')
            q = request.args.get('q')


            if rol_id and int(rol_id) > 0:
                rol_statement = "select * from roles where id=?"
                cur.execute(rol_statement, [rol_id])
                rol = cur.fetchone()       
                return jsonify(rol)         
            elif q:
                if q == '-1':
                    rol_statement = "SELECT roles.id, roles.nombre_rol, roles.descripcion, recursos.ruta_relativa FROM roles left join recursos on recursos.id = roles.homepage order by roles.id limit 10 "
                    cur.execute(rol_statement)
                else:
                    rol_statement = "SELECT roles.id, roles.nombre_rol, roles.descripcion, recursos.ruta_relativa FROM roles left join recursos on recursos.id = roles.homepage where roles.nombre_rol like ? or roles.descripcion like ? "
                    cur.execute(rol_statement, ['%'+q+'%','%'+q+'%'])
                rol_list = cur.fetchall()       
                return jsonify(rol_list)       
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo cargar el registro'}]),500
        else:                      
            cur.close()

    elif request.method == 'PUT':
        try:
            con = connection()
            cur = con.cursor()    
            rol_id = request.form['rol_id']            
            if int(rol_id) > 0:
                rol_statement = "select * from roles where id=?"
                cur.execute(rol_statement, [rol_id])
                rol = cur.fetchone()    
                if rol:
                    nombre_rol = rol[1] if rol[1] == request.form['nombre_rol'] else request.form['nombre_rol'] 
                    descripcion_rol = rol[2] if rol[2] == request.form['descripcion_rol'] else request.form['descripcion_rol']    
                    homepage_rol = rol[3] if rol[3] == request.form['homepage_rol'] else request.form['homepage_rol']    
                    rol_update_statement = "UPDATE roles SET nombre_rol = ?, descripcion = ?, homepage = ? WHERE id = ?" 
                    cur.execute(rol_update_statement, [nombre_rol, descripcion_rol, homepage_rol, rol_id])
                else:
                    raise Exception("No se pudo actualizar el registro")              
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo actualizar el registro'}]),501
        else:    
            con.commit()                  
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue actualizado'}])

@app.route("/admin/settings/recursos", methods=['GET','POST','PUT','DELETE'])
def admin_settings_recursos_rest_resource():
    if request.method == 'DELETE':
        try:
            con = connection()
            cur = con.cursor()        
            recurso_id = request.form['recurso_id']
            recurso_statement = "delete from recursos where id=?"
            cur.execute(recurso_statement, [recurso_id])       
            #con.commit()                
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo eliminar el registro'}]),501
        else:                      
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue eliminado'}])
    
    elif request.method == 'GET':
        try:
            con = connection()
            cur = con.cursor()    
            recurso_id = request.args.get('recurso_id')
            q = request.args.get('q')


            if recurso_id and int(recurso_id) > 0:
                recurso_statement = "select * from recursos where id=?"
                cur.execute(recurso_statement, [recurso_id])
                recurso = cur.fetchone()       
                return jsonify(recurso)         
            elif q:
                if q == '-1':
                    recurso_statement = "SELECT recursos.id, recursos.nombre_recurso, recursos.descripcion, recursos.ruta_relativa FROM recursos order by id asc limit 10"
                    cur.execute(recurso_statement)
                else:
                    recurso_statement = "SELECT recursos.id, recursos.nombre_recurso, recursos.descripcion, recursos.ruta_relativa FROM recursos where recursos.nombre_recurso like ? or recursos.descripcion like ? or recursos.codigo_recurso like ? or recursos.ruta_relativa like ?"
                    cur.execute(recurso_statement, ['%'+q+'%','%'+q+'%','%'+q+'%','%'+q+'%'])
                recurso_list = cur.fetchall()       
                return jsonify(recurso_list)       
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo cargar el registro'}]),500
        else:                      
            cur.close()

    elif request.method == 'PUT':
        try:
            con = connection()
            cur = con.cursor()    
            recurso_id = request.form['recurso_id']            
            if int(recurso_id) > 0:
                recurso_statement = "select * from recursos where id=?"
                cur.execute(recurso_statement, [recurso_id])
                recurso = cur.fetchone()    
                if recurso:
                    nombre_recurso = recurso[1] if recurso[1] == request.form['nombre_recurso'] else request.form['nombre_recurso'] 
                    descripcion_recurso = recurso[2] if recurso[2] == request.form['descripcion_recurso'] else request.form['descripcion_recurso']    
                    codigo_recurso = recurso[3] if recurso[3] == request.form['codigo_recurso'] else request.form['codigo_recurso']    
                    ruta_relativa = recurso[4] if recurso[4] == request.form['ruta_relativa'] else request.form['ruta_relativa'] 
                    recurso_update_statement = "UPDATE recursos SET nombre_recurso = ?, descripcion = ?, codigo_recurso = ?, ruta_relativa = ? WHERE id = ?" 
                    cur.execute(recurso_update_statement, [nombre_recurso, descripcion_recurso, codigo_recurso, ruta_relativa, recurso_id])
                else:
                    raise Exception("No se pudo actualizar el registro")              
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo actualizar el registro'}]),501
        else:    
            con.commit()                  
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue actualizado'}])

@app.route("/admin/settings/paises", methods=['GET','POST','PUT','DELETE'])
def admin_settings_paises_rest_resource():
    if request.method == 'DELETE':
        try:
            con = connection()
            cur = con.cursor()        
            pais_id = request.form['pais_id']
            pais_statement = "delete from paises where id=?"
            cur.execute(pais_statement, [pais_id])       
            #con.commit()                
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo eliminar el registro'}]),501
        else:                      
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue eliminado'}])
    
    elif request.method == 'GET':
        try:
            con = connection()
            cur = con.cursor()    
            pais_id = request.args.get('pais_id')
            q = request.args.get('q')


            if pais_id and int(pais_id) > 0:
                pais_statement = "select * from paises where id=?"
                cur.execute(pais_statement, [pais_id])
                pais = cur.fetchone()       
                return jsonify(pais)         
            elif q:
                if q == '-1':
                    pais_statement = "SELECT paises.id, paises.nombre, paises.descripcion FROM paises order by id asc limit 10"
                    cur.execute(pais_statement)
                else:
                    pais_statement = "SELECT paises.id, paises.nombre, paises.descripcion FROM paises where paises.nombre like ? or paises.descripcion like ? "
                    cur.execute(pais_statement, ['%'+q+'%','%'+q+'%'])
                pais_list = cur.fetchall()       
                return jsonify(pais_list)       
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo cargar el registro'}]),500
        else:                      
            cur.close()

    elif request.method == 'PUT':
        try:
            con = connection()
            cur = con.cursor()    
            pais_id = request.form['pais_id']            
            if int(pais_id) > 0:
                pais_statement = "select * from paises where id=?"
                cur.execute(pais_statement, [pais_id])
                pais = cur.fetchone()    
                if pais:
                    nombre_pais = pais[1] if pais[1] == request.form['nombre_pais'] else request.form['nombre_pais'] 
                    descripcion_pais = pais[2] if pais[2] == request.form['descripcion_pais'] else request.form['descripcion_pais']    
                    pais_update_statement = "UPDATE paises SET nombre = ?, descripcion = ? WHERE id = ?" 
                    cur.execute(pais_update_statement, [nombre_pais, descripcion_pais, pais_id])
                else:
                    raise Exception("No se pudo actualizar el registro")              
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo actualizar el registro'}]),501
        else:    
            con.commit()                  
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue actualizado'}])

@app.route("/admin/settings/departamentos", methods=['GET','POST','PUT','DELETE'])
def admin_settings_departamentos_rest_resource():
    if request.method == 'DELETE':
        try:
            con = connection()
            cur = con.cursor()        
            departamento_id = request.form['departamento_id']
            departamento_statement = "delete from departamentos where id=?"
            cur.execute(departamento_statement, [departamento_id])       
            #con.commit()                
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo eliminar el registro'}]),501
        else:                      
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue eliminado'}])
    
    elif request.method == 'GET':
        try:
            con = connection()
            cur = con.cursor()    
            departamento_id = request.args.get('departamento_id')
            q = request.args.get('q')


            if departamento_id and int(departamento_id) > 0:
                departamento_statement = "select * from departamentos where id=?"
                cur.execute(departamento_statement, [departamento_id])
                departamento = cur.fetchone()       
                return jsonify(departamento)         
            elif q:
                if q == '-1':
                    departamento_statement = "SELECT departamentos.id, departamentos.nombre, paises.nombre FROM departamentos inner join paises on paises.id = departamentos.paises_id order by departamentos.id asc limit 10"
                    cur.execute(departamento_statement)
                else:
                    departamento_statement = "SELECT departamentos.id, departamentos.nombre, paises.nombre FROM departamentos inner join paises on paises.id = departamentos.paises_id where departamentos.nombre like ? or departamentos.descripcion like ? or paises.nombre like ?"
                    cur.execute(departamento_statement, ['%'+q+'%','%'+q+'%','%'+q+'%'])
                departamento_list = cur.fetchall()       
                return jsonify(departamento_list)       
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo cargar el registro'}]),500
        else:                      
            cur.close()

    elif request.method == 'PUT':
        try:
            con = connection()
            cur = con.cursor()    
            departamento_id = request.form['departamento_id']            
            if int(departamento_id) > 0:
                departamento_statement = "select * from departamentos where id=?"
                cur.execute(departamento_statement, [departamento_id])
                departamento = cur.fetchone()    
                if departamento:
                    nombre_departamento = departamento[1] if departamento[1] == request.form['nombre_departamento'] else request.form['nombre_departamento'] 
                    descripcion_departamento = departamento[2] if departamento[2] == request.form['descripcion_departamento'] else request.form['descripcion_departamento']    
                    pais_departamento = departamento[3] if departamento[3] == request.form['pais_departamento'] else request.form['pais_departamento']    
                    departamento_update_statement = "UPDATE departamentos SET nombre = ?, descripcion = ?, paises_id = ? WHERE id = ?" 
                    cur.execute(departamento_update_statement, [nombre_departamento, descripcion_departamento, pais_departamento, departamento_id])
                else:
                    raise Exception("No se pudo actualizar el registro")              
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo actualizar el registro'}]),501
        else:    
            con.commit()                  
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue actualizado'}])

@app.route("/admin/settings/municipios", methods=['GET','POST','PUT','DELETE'])
def admin_settings_municipios_rest_resource():
    if request.method == 'DELETE':
        try:
            con = connection()
            cur = con.cursor()        
            municipio_id = request.form['municipio_id']
            municipio_statement = "delete from municipios where id=?"
            cur.execute(municipio_statement, [municipio_id])       
            #con.commit()                
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo eliminar el registro'}]),501
        else:                      
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue eliminado'}])
    
    elif request.method == 'GET':
        try:
            con = connection()
            cur = con.cursor()    
            municipio_id = request.args.get('municipio_id')
            q = request.args.get('q')


            if municipio_id and int(municipio_id) > 0:
                municipio_statement = "select * from municipios where id=?"
                cur.execute(municipio_statement, [municipio_id])
                municipio = cur.fetchone()       
                return jsonify(municipio)         
            elif q:
                if q == '-1':
                    municipio_statement = "SELECT municipios.id, municipios.nombre, departamentos.nombre FROM municipios inner join departamentos on departamentos.id = municipios.departamentos_id order by municipios.id asc limit 10"
                    cur.execute(municipio_statement)
                else:
                    municipio_statement = "SELECT municipios.id, municipios.nombre, departamentos.nombre FROM municipios inner join departamentos on departamentos.id = municipios.departamentos_id where municipios.nombre like ? or municipios.descripcion like ? or departamentos.nombre like ?"
                    cur.execute(municipio_statement, ['%'+q+'%','%'+q+'%','%'+q+'%'])
                municipio_list = cur.fetchall()       
                return jsonify(municipio_list)       
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo cargar el registro'}]),500
        else:                      
            cur.close()

    elif request.method == 'PUT':
        try:
            con = connection()
            cur = con.cursor()    
            municipio_id = request.form['municipio_id']            
            if int(municipio_id) > 0:
                municipio_statement = "select * from municipios where id=?"
                cur.execute(municipio_statement, [municipio_id])
                municipio = cur.fetchone()    
                if municipio:
                    nombre_municipio = municipio[1] if municipio[1] == request.form['nombre_municipio'] else request.form['nombre_municipio'] 
                    descripcion_municipio = municipio[2] if municipio[2] == request.form['descripcion_municipio'] else request.form['descripcion_municipio']    
                    departamento_municipio = municipio[3] if municipio[3] == request.form['departamento_municipio'] else request.form['departamento_municipio']    
                    municipio_update_statement = "UPDATE municipios SET nombre = ?, descripcion = ?, departamentos_id = ? WHERE id = ?" 
                    cur.execute(municipio_update_statement, [nombre_municipio, descripcion_municipio, departamento_municipio, municipio_id])
                else:
                    raise Exception("No se pudo actualizar el registro")              
        except:
            return jsonify([{ 'status': 'error', 'message': 'No se pudo actualizar el registro'}]),501
        else:    
            con.commit()                  
            cur.close() 
            return jsonify([{ 'status': 'ok', 'message': 'El registro seleccionado fue actualizado'}])

if __name__ == '__main__':
    app.run(debug=True)