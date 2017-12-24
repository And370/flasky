from flask import render_template, session, redirect, url_for, current_app, abort, flash, request
from .. import db
from ..models import User, Permission, Role
from ..email import send_email
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from ..decorators import admin_required, permission_required
from flask_login import login_required, current_user
import base64


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASK_ADMIN']:
                send_email(current_app.config['FLASK_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


@main.route('/try')
def try_1():
    return render_template('try.html')


@main.route('/user/<username>')
def user(username):
    the_user = User.query.filter_by(username=username).first()
    if the_user is None:  # base64.b64encode(user.head_portrait).split()
        abort(403)  # str(base64.b64encode(a2.read()))[1:].replace("'","")
    head_portrait = str(base64.b64encode(the_user.head_portrait))[1:].replace("'", "")
    return render_template('user.html', user=the_user, head_portrait=head_portrait)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        '''
        user = current_user(name=form.name.data,
                            location=form.location.data,
                            about_me=form.about_me.data)
        '''
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        current_user.head_portrait = request.files['head_portrait'].read()  # bytes' data  ↑b64encode
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    form.head_portrait = current_user.head_portrait
    return render_template('edit_profile.html', form=form)


@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    the_user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=the_user)
    if form.validate_on_submit():
        # name location about_me email username role confirmed   7
        the_user.name = form.name.data
        the_user.location = form.location.data
        the_user.about_me = form.about_me.data
        the_user.email = form.email.data
        the_user.username = form.username.data
        the_user.role = Role.query.get(form.role.data)  # it is "role_id" in the form
        the_user.confirmed = form.confirmed.data
        db.session.add(the_user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=the_user.username))
    form.name.data = the_user.name
    form.location.data = the_user.location
    form.about_me.data = the_user.about_me
    form.email.data = the_user.email
    form.username.data = the_user.username
    form.role.data = the_user.role_id
    form.confirmed.data = the_user.confirmed
    return render_template('edit_profile.html', form=form, user=the_user)


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return 'For administrators!'


@main.route('/moderators')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return 'For comment moderators!'
