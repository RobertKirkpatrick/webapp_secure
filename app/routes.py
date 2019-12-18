from flask import render_template, flash, url_for, redirect, request
from app import app
from app.forms import LoginForm, spellcheckForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, SpellCheckC
from flask_login import login_required
from app import db
from app.forms import RegistrationForm
from werkzeug.urls import url_parse
import subprocess, os, sys, os.path
from flask_wtf.csrf import CSRFProtect, CSRFError

'''
#create admin account
if User.query.filter_by(username='admin').first() == None:
    admin = User(username ='admin', twofact='17577485533') # also set to admin once added
    admin.set_password('password')
    db.session.add(admin)
    db.session.commit()
'''
@app.route('/')
@app.route('/index')
@login_required   # this url becomes protected with user requiring login to see it
def index():
    # render_template invokes jinja2 template engine
    return render_template('index.html', title='Home')
    # return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # identify if user is already authenticated, and if so redirect to index
    login_message = ''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # method validate_on_submit does the processing, GET will return false, skipping if statement
        # POST submit is going to gather data, run validators, and return True, ready to be processed
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            login_message = 'Incorrect'
            return render_template('login.html', title='Login', result=login_message, form=form)
            #return redirect(url_for('login'))
        if user.twofact != form.twofact.data:
            login_message = 'Incorrect'
            return render_template('login.html', title='Login', result=login_message, form=form)
        login_user(user)  # , remember=form.remember_me.data)
        # next_page = request.args.get('next')
        login_message = 'Success'
        #if not next_page or url_parse(next_page).netloc != '':
            # if there is not a next in the url or if the url is to a different domain, then redirect to index
        #    next_page = url_for('index')
        #return redirect(next_page)  # otherwise redirect to the next page
    return render_template('login.html', title='Login', result=login_message, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_message = ''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        userl = User(username=form.username.data, twofact=form.twofact.data)
        userl.set_password(form.password.data)
        db.session.add(userl)
        db.session.commit()
        registration_message = 'success'
        flash('Congratulations, you are now a registered user!')
        #return redirect(url_for('login'))
    else:
        registration_message = 'failure'
    return render_template('register.html', success=registration_message, form=form)


@app.route('/spell_check', methods=['GET', 'POST'])
@login_required   # this url becomes protected with user requiring login to see it
def spell_check():
    form = spellcheckForm()
    if form.validate_on_submit():
        user_words = form.spellcheck.data
        ifile = open('check_words.txt', "w")
        ifile.write(user_words)
        ifile.close()
        # PIPE indicates that a pipe to the standard stream should be opened. Most useful with Popen.communicate().
        pwd = os.getcwd()
        words = subprocess.Popen(['./a.out', 'check_words.txt', 'wordlist.txt'], cwd=pwd, stdout=subprocess.PIPE)
        stdoutdata, stderrdata = words.communicate()
        found_mispelled = stdoutdata.decode("utf-8").rstrip()
        new_query = SpellCheckC(uname = current_user.id, query_word = user_words, query_result=found_mispelled)
        db.session.add(new_query)
        db.session.commit()
        flash('Success')
        return render_template('spell_check.html', title='Spell Check',
                               user_words=user_words, misspelled=found_mispelled, form=form)
    result = None
    return render_template('spell_check.html', title='Spell Check', form=form)
