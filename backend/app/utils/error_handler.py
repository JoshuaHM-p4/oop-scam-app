from flask import jsonify

def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def register_error_handlers(app):
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_server_error)