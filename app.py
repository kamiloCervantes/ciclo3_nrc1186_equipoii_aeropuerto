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
    pais = SelectField(u'Pais', coerce=int, validate_choice=False)
    departamento = SelectField(u'Departamento', choices=[('1', 'Córdoba'), ('1', 'Antioquia'), ('2', 'Cundinamarca')])
    ciudad = SelectField(u'Ciudad', choices=[('1', 'Montería'), ('1', 'Cereté'), ('2', 'Ciénaga de Oro')])
  
   

@app.route("/admin/locations/add", methods=['GET','POST'])
def locations_add():
    form = locations_add_form()
    con = connection()
    cur = con.cursor()
    paises_statement = "SELECT id, nombre from paises"
    cur.execute(paises_statement)
    paises_list = cur.fetchall()
    form.pais.choices = paises_list
    cur.close()
    if form.validate_on_submit():
        return redirect(url_for('admin_dashboard'))
    return render_template('locations_add.html', form=form)


class users_add_form(FlaskForm):
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

class users_edit_form(FlaskForm):
    nombrecompleto = StringField('nombre', validators=[InputRequired(message='El nombre es requerido'), Length(min=5, max=50, message='El nombre debe tener entre 5 y 50 caracteres')])
    tipodocumento = SelectField(u'Tipo de documento', choices=[('C.C.', 'C.C.'), ('C.E.', 'C.E.'), ('T.I.', 'T.I.')], validate_choice=False)
    numdocumento = StringField('numdocumento', validators=[InputRequired(message='El número de documento es requerido')])
    correoelectronico = StringField('correoelectronico', validators=[InputRequired(message='El email es requerido'), Length(min=5, max=50, message='El email debe tener entre 5 y 50 caracteres'), Email(message='Debe ingresar un email valido')])


@app.route("/admin/users/add", methods=['GET','POST'])
def users_add():
    form = users_add_form()
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
        usuario_statement = "INSERT INTO usuarios (username, password, activo, personas_id)  VALUES (?,?,?,?)"
        cur.execute(usuario_statement, [form.username.data, hash_func.hexdigest(), '1', personas_id])
        usuarios_id = cur.lastrowid
        roles_statement = "INSERT INTO usuarios_has_roles (usuarios_id,roles_id) VALUES (?,?)"
        cur.execute(roles_statement, [usuarios_id, form.rol.data])
        cur.close()
        con.commit()
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

@app.route("/admin/settings")
def admin_settings():
    con = connection()
    cur = con.cursor()
    roles_form = settings_roles_form()
    roles_form_edit = settings_roles_form_edit()
    rol_statement = "SELECT roles.id, roles.nombre_rol, roles.descripcion, recursos.ruta_relativa FROM roles left join recursos on recursos.id = roles.homepage ORDER BY roles.id ASC LIMIT 10"
    cur.execute(rol_statement)
    roles = cur.fetchall()
    resources_statement = "select id,ruta_relativa from recursos"
    cur.execute(resources_statement)
    resources_list = cur.fetchall() 
    roles_form.homepage.choices = resources_list
    roles_form_edit.homepage_edit.choices = resources_list
    cur.close()
    return render_template("admin_settings.html",roles_form=roles_form, roles_form_edit=roles_form_edit, roles_list=roles)  

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




if __name__ == '__main__':
    app.run(debug=True)