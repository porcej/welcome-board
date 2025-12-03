from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import users_bp
from ..extensions import db
from ..models import User
from ..forms.users import UserForm


def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Admin access required", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


@users_bp.route("/")
@admin_required
def list_users():
    users = User.query.order_by(User.email).all()
    return render_template("users/index.html", users=users)


@users_bp.route("/new", methods=["GET", "POST"])
@admin_required
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        if not form.password.data:
            flash("Password is required for new users", "danger")
            return render_template("users/form.html", form=form, title="New User")
        
        user = User(
            email=form.email.data.lower().strip(),
            is_admin=form.is_admin.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"User {user.email} created successfully", "success")
        return redirect(url_for("users.list_users"))
    return render_template("users/form.html", form=form, title="New User")


@users_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    # Prevent editing yourself to avoid locking yourself out
    if user.id == current_user.id:
        flash("You cannot edit your own account from this page", "warning")
        return redirect(url_for("users.list_users"))
    
    form = UserForm(obj=user, user=user)
    if form.validate_on_submit():
        user.email = form.email.data.lower().strip()
        user.is_admin = form.is_admin.data
        
        # Only update password if a new one is provided
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        flash(f"User {user.email} updated successfully", "success")
        return redirect(url_for("users.list_users"))
    return render_template("users/form.html", form=form, title="Edit User", user=user)


@users_bp.route("/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # Prevent deleting yourself
    if user.id == current_user.id:
        flash("You cannot delete your own account", "danger")
        return redirect(url_for("users.list_users"))
    
    email = user.email
    db.session.delete(user)
    db.session.commit()
    flash(f"User {email} deleted successfully", "success")
    return redirect(url_for("users.list_users"))

