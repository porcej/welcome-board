from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required
from . import icons_bp
from ..extensions import db
from ..models import Icon
from ..forms.icons import IconForm
import os
from werkzeug.utils import secure_filename


@icons_bp.route("/")
@login_required
def list_icons():
    icons = Icon.query.order_by(Icon.name).all()
    return render_template("icons/index.html", icons=icons)


@icons_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_icon():
    form = IconForm()
    if form.validate_on_submit():
        icon = Icon(
            name=form.name.data,
            enabled=form.enabled.data if form.enabled.data is not None else True
        )
        
        if form.use_text.data:
            icon.characters = form.characters.data
            icon.font = form.font.data
        else:
            # Handle image upload
            file = form.image.data
            if file:
                os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
                filename = secure_filename(file.filename)
                path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                file.save(path)
                rel = os.path.relpath(path, os.path.join(current_app.root_path, "static"))
                icon.image_path = rel.replace("\\", "/")
        
        db.session.add(icon)
        db.session.commit()
        flash("Icon created", "success")
        return redirect(url_for("icons.list_icons"))
    return render_template("icons/form.html", form=form, title="New Icon")


@icons_bp.route("/<int:icon_id>/edit", methods=["GET", "POST"])
@login_required
def edit_icon(icon_id: int):
    icon = Icon.query.get_or_404(icon_id)
    form = IconForm(obj=icon, icon=icon)
    form.use_text.data = icon.characters is not None
    
    if form.validate_on_submit():
        icon.name = form.name.data
        icon.enabled = form.enabled.data if form.enabled.data is not None else True
        
        if form.use_text.data:
            icon.characters = form.characters.data
            icon.font = form.font.data
            icon.image_path = None  # Clear image if switching to text
        else:
            # Handle image upload
            file = form.image.data
            if file:
                os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
                filename = secure_filename(file.filename)
                path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                file.save(path)
                rel = os.path.relpath(path, os.path.join(current_app.root_path, "static"))
                icon.image_path = rel.replace("\\", "/")
            elif not icon.image_path:
                # If no new image and no existing image, require one
                flash("Either upload an image or use text.", "error")
                return render_template("icons/form.html", form=form, title="Edit Icon", icon=icon)
            icon.characters = None
            icon.font = None
        
        db.session.commit()
        flash("Icon updated", "success")
        return redirect(url_for("icons.list_icons"))
    return render_template("icons/form.html", form=form, title="Edit Icon", icon=icon)


@icons_bp.route("/<int:icon_id>/delete", methods=["POST"])
@login_required
def delete_icon(icon_id: int):
    icon = Icon.query.get_or_404(icon_id)
    db.session.delete(icon)
    db.session.commit()
    flash("Icon deleted", "success")
    return redirect(url_for("icons.list_icons"))

