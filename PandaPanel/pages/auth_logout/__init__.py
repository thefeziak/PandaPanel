from flask import Blueprint, redirect
from flask_login import login_required, logout_user

bp = Blueprint('auth_logout', __name__)

@bp.route('/auth/logout')
@login_required
def auth_login():
    logout_user()
    return redirect("/")