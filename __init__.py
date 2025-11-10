import os
from flask import Flask, render_template


def create_app(test_config=None):
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)
    
    # Get configuration from environment variables (for production) or use defaults
    secret_key = os.environ.get('SECRET_KEY', 'dev')
    database_url = os.environ.get('DATABASE_URL')
    
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        DATABASE=os.path.join(app.instance_path, 'Deplacity.sqlite'),
        DATABASE_URL=database_url  # PostgreSQL URL for production
    )

    from .blueprints import statistique, requete, home, admin, citymap
    app.register_blueprint(home.bp)
    app.register_blueprint(statistique.bp)
    app.register_blueprint(requete.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(citymap.bp)
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/statistique', endpoint='statistique')
    app.add_url_rule('/requetes', endpoint='requetes')
    app.add_url_rule('/admin', endpoint='connexion')
    app.add_url_rule('/citymap', endpoint='citymap')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route("/ourteam")
    def team():
        return render_template('team.html')
    
    @app.route('/dikete')
    def dikete():
        return render_template('dikete.html')
    
    from .utils import csv_file
    @app.before_request
    def fill_db():
        csv_file.write_in_db()
        app.before_request_funcs[None] = [
            func for func in app.before_request_funcs[None] if func != fill_db]

    from .utils import db
    db.init_app(app)

    with app.app_context():
        db.init_db()
    
    return app
