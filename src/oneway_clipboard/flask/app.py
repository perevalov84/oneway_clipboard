from flask import Flask, jsonify

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config:
        app.config.update(test_config)
        app.debug = True

    @app.route('/health')
    def health():
        return jsonify({"status":"ok"})
    

    from . import blueprint
    app.register_blueprint(blueprint.bp)

    return app