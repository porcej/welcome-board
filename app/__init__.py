import os
from flask import Flask, request, redirect, url_for, render_template
from flask_login import current_user
from .extensions import db, migrate, login_manager, csrf
from .config import get_config


def register_blueprints(app: Flask) -> None:
    # Blueprints imported inside function to avoid circular imports
    from .auth.routes import auth_bp
    from .schedules.routes import schedules_bp
    from .display.routes import display_bp
    from .icons.routes import icons_bp
    from .users.routes import users_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(schedules_bp, url_prefix="/schedules")
    app.register_blueprint(display_bp, url_prefix="/display")
    app.register_blueprint(icons_bp, url_prefix="/icons")
    app.register_blueprint(users_bp, url_prefix="/users")


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists (for SQLite default path)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    app.config.from_object(get_config())

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    register_blueprints(app)

    @app.template_filter('hex_to_rgb')
    def hex_to_rgb_filter(hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (33, 37, 41)  # default dark gray

    @app.before_request
    def enforce_login_for_admin():
        # Allow public display and static assets without auth
        if request.endpoint in ("static",):
            return None
        path = request.path or ""
        if path.startswith("/display"):
            return None
        # Allow auth pages
        if request.endpoint and request.endpoint.startswith("auth."):
            return None
        # Redirect anonymous users to login
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))

    # CLI: create admin user
    @app.cli.command("create-admin")
    def create_admin():
        from .models import User
        import getpass
        email = input("Admin email: ").strip().lower()
        if not email:
            print("Email required")
            return
        if User.query.filter_by(email=email).first():
            print("User already exists")
            return
        password = getpass.getpass("Password: ")
        if not password:
            print("Password required")
            return
        user = User(email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Admin user {email} created.")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


