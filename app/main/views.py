from flask import render_template, session, redirect, url_for, current_app, abort, flash, request
from .. import db
from ..models import User, Permission, Role
from . import main
from .forms import EditProfileForm, EditProfileAdminForm
from ..decorators import admin_required, permission_required
from flask_login import login_required, current_user
import base64
from flasky import photos
from flask_uploads import UploadNotAllowed


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:  # 如果已登录，则传入头像二进制数据流并显示头像
        return render_template('index.html', username=current_user.username)
        # head_portrait=head_portrait)
    return render_template('index.html')


'''
@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user:
        the_user = User.query.filter_by(username=form.name.data).first()
        if the_user is None:
            the_user = User(username=form.name.data)
            db.session.add(the_user)
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
'''


@main.route('/baidumap')
def baidu_map():
    return render_template('baidumap.html')


'''
@main.route('/image/<username>')
def image(username):
    the_user = User.query.filter_by(username=username).first()
    if the_user is None:
        abort(403)
    image_url = photos.url(the_user.head_portrait)
    return render_template('image.html', image_url=image_url, username=the_user.username)
'''


@main.route('/user/<username>')
def user(username):
    the_user = User.query.filter_by(username=username).first()
    if the_user is None:  # base64.b64encode(user.head_portrait).split()
        abort(404)  # str(base64.b64encode(a2.read()))[1:].replace("'","")
        # head_portrait = str(base64.b64encode(the_user.head_portrait))[1:].replace("'", "")

        # image_url = photos.url(the_user.head_portrait)
    return render_template('user.html', user=the_user)

    # return render_template('user.html', user=the_user)
    # head_portrait=head_portrait)


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

        # current_user.head_portrait = request.files['head_portrait'].read()  # bytes' data  ↑b64encode
        # 保存表单内提交的文件并返回文件名

        try:
            current_user.name = form.name.data
            current_user.location = form.location.data
            current_user.about_me = form.about_me.data
            current_user.head_portrait = photos.url(photos.save(request.files['head_portrait'],
                                                                name=current_user.username + '.'))
        except UploadNotAllowed as e:
            abort(413)
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
        # except: raise UploadNotAllowed

        # image_url = photos.url(current_user.head_portrait)
        # head_portrait = str(base64.b64encode(current_user.head_portrait))[1:].replace("'", "")
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
        try:
            the_user.name = form.name.data
            the_user.location = form.location.data
            the_user.about_me = form.about_me.data
            the_user.email = form.email.data
            the_user.username = form.username.data
            the_user.role = Role.query.get(form.role.data)  # it is "role_id" in the form
            the_user.confirmed = form.confirmed.data
            the_user.head_portrait = photos.url(photos.save(request.files['head_portrait'],
                                                            name=current_user.username + '.'))
            db.session.add(the_user)
            db.session.commit()
            flash('The profile has been updated.')
            return redirect(url_for('.user', username=the_user.username))
        except UploadNotAllowed as e:
            flash('xxx')
    form.name.data = the_user.name
    form.location.data = the_user.location
    form.about_me.data = the_user.about_me
    form.email.data = the_user.email
    form.username.data = the_user.username
    form.role.data = the_user.role_id
    form.confirmed.data = the_user.confirmed
    form.head_portrait.data = the_user.head_portrait
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
