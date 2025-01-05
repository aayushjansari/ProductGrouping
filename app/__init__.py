from flask import Flask
import os

def create_app():

    app = Flask(__name__, template_folder="../templates", static_folder='static', static_url_path='/static')
    # Ensure directories exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    # Configure app
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['OUTPUT_FOLDER'] = 'static'


    # Serve uploaded and static files
    from flask import send_from_directory
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory('uploads', filename)

    @app.route('/static/<filename>')
    def static_file(filename):
        return send_from_directory('static', filename)

    
    # Register routes
    with app.app_context():
        from .routes import main_blueprint
        app.register_blueprint(main_blueprint)

    return app
