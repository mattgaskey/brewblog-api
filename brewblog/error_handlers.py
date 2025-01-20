from flask import jsonify
from brewblog.auth import AuthError

def register_error_handlers(bp):
    @bp.errorhandler(400)
    def bad_request(error):
        response = jsonify({'error': 'Bad Request', 'message': str(error)})
        response.status_code = 400
        return response

    @bp.errorhandler(401)
    def unauthorized(error):
        response = jsonify({'error': 'Unauthorized', 'message': str(error)})
        response.status_code = 401
        return response

    @bp.errorhandler(403)
    def forbidden(error):
        response = jsonify({'error': 'Forbidden', 'message': str(error)})
        response.status_code = 403
        return response

    @bp.errorhandler(404)
    def not_found(error):
        response = jsonify({'error': 'Not Found', 'message': str(error)})
        response.status_code = 404
        return response

    @bp.errorhandler(500)
    def internal_server_error(error):
        response = jsonify({'error': 'Internal Server Error', 'message': str(error)})
        response.status_code = 500
        return response
    
    @bp.errorhandler(AuthError)
    def handle_auth_error(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response