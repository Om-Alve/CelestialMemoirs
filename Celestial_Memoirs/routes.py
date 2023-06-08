from flask import render_template,redirect,url_for,flash,request
from Celestial_Memoirs.forms import LoginForm,RegisterForm,PostForm
from Celestial_Memoirs import app
from Celestial_Memoirs.models import Users,Entries
from Celestial_Memoirs import bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
from sqlalchemy.sql.expression import desc



@app.route('/')
def about():
    return render_template('about_us.html')

@app.route('/home')
@login_required
def home():
    entries = Entries.query.filter_by(author=current_user).order_by(desc(Entries.date)).all()
    return render_template('home.html',entries = entries)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!','info')
        return redirect('/home')
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html',form = form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    return render_template('register.html',form=form)

@app.route('/create_entry')
def create_entry():
    return render_template('create_post.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route("/entry/new", methods=['GET', 'POST'])
@login_required
def new_entry():
    form = PostForm()
    if form.validate_on_submit():
        entry = Entries(date=form.date.data, content=form.content.data, author=current_user)
        db.session.add(entry)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html',
                           form=form, legend='New Post')


@app.route('/entry/<int:entry_id>')
@login_required
def entry(entry_id):
    entry = Entries.query.get_or_404(entry_id)
    if entry.author != current_user:
        return redirect(url_for('home'))
    return render_template('entry.html',entry=entry)

@app.route('/entry/<int:entry_id>/update',methods=['GET','POST'])
@login_required
def update_entry(entry_id):
    form = PostForm()
    entry = Entries.query.get_or_404(entry_id)
    if entry.author != current_user:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        entry.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('entry',entry_id=entry_id))
    elif request.method == 'GET':
        form.date.data = entry.date
        form.content.data = entry.content
    return render_template('update_post.html',
                           form=form, legend='Update Post')

@app.route("/entry/<int:entry_id>/delete", methods=['POST','GET'])
@login_required
def delete_entry(entry_id):
    entry = Entries.query.get_or_404(entry_id)
    if entry.author != current_user:
        return redirect(url_for('home'))
    db.session.delete(entry)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

