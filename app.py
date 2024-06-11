from flask import Flask, g, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin, login_required, LoginManager, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
import bcrypt
import sqlite3
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'], detect_types= sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.executescript(f.read())

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.cli.command('init-db')
def init_db_command():
    init_db()
    print('Initialized the database.')
'''
@app.route('/')
def index():
    return render_template('index.html')
'''

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#users classes
class Student(UserMixin):
    def __init__(self, id, matricule, nom, prenom,date_de_naissance ,email, mot_de_passe):
        self.id = id
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.email = email
        self.mot_de_passe = mot_de_passe
class Admin(UserMixin):
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username    
        self.password = password
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    
    db = get_db()
    cur = db.execute('SELECT * FROM etudiant WHERE etudiant_id = ?', (user_id,)).fetchone()
    if cur is not None:
        return Student(cur['etudiant_id'], cur['matricule'], cur['nom'], cur['prenom'], cur['email'], cur['date_de_naissance'],cur['mot_de_passe'])
    cur = db.execute('SELECT * FROM admin WHERE admin_id = ?', (user_id,)).fetchone()
    if cur is not None:
        return Admin(cur['admin_id'], cur['username'], cur['password'], cur.get('email'))
    return None

#forms classes
class StudentLoginForm(FlaskForm):
    matricule = StringField(validators=[InputRequired(), 
                Length(min=4, max=20)], 
                render_kw={"placeholder": "matricule"})
    password = PasswordField(validators=[InputRequired(), 
                    Length(min=4, max=80)], 
                    render_kw={"placeholder": "password"})
    submit = SubmitField('submit')

class AdminLoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), 
                Length(min=4, max=20)], 
                render_kw={"placeholder": "username"})
    password = PasswordField(validators=[InputRequired(), 
                    Length(min=4, max=80)], 
                    render_kw={"placeholder": "password"})
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    matricule = StringField(validators=[InputRequired(), 
                Length(min=4, max=20)], 
                render_kw={"placeholder": "matricule"})
    search = SubmitField('search')
class NoteForm(FlaskForm):
    note = StringField(validators=[InputRequired()], 
            render_kw={"placeholder": "note"})
    submit = SubmitField('submit')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    
    student_form = StudentLoginForm()
    if student_form.validate_on_submit():
        db = get_db()
        cur = db.execute('SELECT * FROM etudiant WHERE matricule = ?', (student_form.matricule.data,)).fetchone()

        if cur is None:
            flash('Invalid matricule')
        elif not verify_password(student_form.password.data, cur['mot_de_passe']):
            
            flash('Invalid password')
        else:
            user =  Student(cur['etudiant_id'], cur['matricule'], cur['nom'], cur['prenom'], cur['email'], cur['date_de_naissance'],cur['mot_de_passe'])
            login_user(user)
            return redirect(url_for('student'))
    
    admin_form = AdminLoginForm()
    if admin_form.validate_on_submit():
        db = get_db()
        cur = db.execute('SELECT * FROM admin WHERE username = ?', (admin_form.username.data,)).fetchone()
        if cur is None:
            flash('Invalid username')
        elif not verify_password(admin_form.password.data, cur['password']):
            flash('Invalid password')
        else:
            user = Admin(cur['admin_id'], cur['username'], cur['password'], cur['email'])
            login_user(user)
            return redirect(url_for('admin'))
    
    return render_template('login.html', student_form=student_form, admin_form=admin_form)

@app.route("/student", methods=["POST", "GET"])
@login_required
def student():
    name = current_user.nom + ' ' + current_user.prenom
    return render_template('student.html', student_name=name)

@app.route("/admin", methods=["POST", "GET"])
@login_required
def admin():
    return render_template('admin.html')

@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/Information', methods=["POST", "GET"])
@login_required
def information():
    first_name = current_user.prenom
    last_name = current_user.nom
    id = current_user.matricule
    date_of_birth = current_user.date_de_naissance
    return render_template('information.html', first_name=first_name, last_name=last_name, id=id, date_of_birth=date_of_birth)

@app.route('/group', methods=["POST", "GET"])
@login_required
def group():
    first_name = current_user.prenom
    last_name = current_user.nom
    id = current_user.id
    db = get_db()
    cur = db.execute('''SELECT g.nom_group
                        FROM etudiant e
                        JOIN etudiant_groups eg ON e.etudiant_id = eg.etudiant_id
                        JOIN groups g ON eg.group_id = g.group_id
                        WHERE e.etudiant_id = ?''', (id,)).fetchone()
    group = cur['nom_group']
    return render_template('group.html', first_name=first_name, last_name=last_name, group=group)

@app.route('/note_ex', methods=["POST", "GET"])
@login_required
def note_ex():
    id = current_user.id
    db = get_db()
    cur = db.execute('''SELECT 
                        m.module AS module,
                        m.coefficient AS coef,
                        i.note_controle AS note
                         FROM 
                        inscription i
                        JOIN 
                        modules m ON i.module_id = m.module_id
                        WHERE 
                        i.etudiant_id = ?''', (id,)).fetchall()
    
    return render_template('note_ex.html', data=cur)

@app.route('/note_td', methods=["POST", "GET"])
@login_required
def note_td():
    id = current_user.id
    db = get_db()
    cur = db.execute('''SELECT 
                        m.module AS module,
                        m.coefficient AS coef,
                        i.note_td AS note
                        FROM 
                        inscription i
                        JOIN 
                        modules m ON i.module_id = m.module_id
                        WHERE 
                        i.etudiant_id = ?''', (id,)).fetchall()
    
    return render_template('note_td.html', data=cur)

@app.route('/absence', methods=["POST", "GET"])
@login_required
def absence():
    id = current_user.id
    db = get_db()
    cur = db.execute('''sELECT 
                        m.module AS module,
                        a.absence_count AS absences
                        FROM 
                        absences a
                        JOIN 
                        modules m ON a.module_id = m.module_id
                        WHERE 
                        a.etudiant_id = ?''', (id,)).fetchall()
    
    return render_template('absence.html', data=cur)

@app.route('/add_ex', methods=["POST", "GET"])
@login_required
def add_ex():
    search_form = SearchForm()
    note_form = NoteForm()
    db = get_db()
    modules = db.execute('SELECT module_id, module, coefficient FROM modules').fetchall()

    if request.method == 'POST' and 'search' in request.form and search_form.validate_on_submit():
        matricule = search_form.matricule.data
        cur = db.execute('SELECT * FROM etudiant WHERE matricule = ?', (matricule,)).fetchone()
        
        if cur is None:
            flash('Student not found', 'danger')
            return redirect(url_for('add_ex'))
        
        student_id = cur['etudiant_id']
        flash('Student found', 'success')
        return render_template('add_ex.html', search_form=search_form, note_form=note_form, modules=modules, student=cur)
    
    elif request.method == 'POST' and 'send' in request.form and note_form.validate_on_submit():
        print('student_id == ', student_id)
        for module in modules:
            module_id = module['module_id']
            note_controle = request.form.get(f'note_{module_id}')
            db.execute('''
                INSERT OR REPLACE INTO inscription (etudiant_id, module_id, note_controle)
                VALUES (?, ?, ?)
            ''', (student_id, module_id, note_controle))
        db.commit()
        flash('Notes updated successfully', 'success')
        return redirect(url_for('add_ex'))
    
    return render_template('add_ex.html', search_form=search_form, note_form=note_form, modules=modules, student=None)




if __name__ == '__main__':
    app.run(debug=True)
