"""
This module defines error handlers for various HTTP errors and authentication errors.
These handlers are registered to a Flask blueprint to provide consistent error responses.
"""

from flask import jsonify
from brewblog.auth import AuthError

def register_error_handlers(bp):
    """
    Registers error handlers for the Flask blueprint.

    Args:
        bp (Blueprint): The Flask blueprint to register the error handlers on.
    """
    @bp.errorhandler(400)
    def bad_request(error):
        """
        Handles 400 Bad Request errors.

        Args:
            error (HTTPException): The HTTP exception raised.

        Returns:
            Response: The JSON response with error details.
        """
        response = jsonify({'error': 'Bad Request', 'message': str(error)})
        response.status_code = 400
        return response

    @bp.errorhandler(401)
    def unauthorized(error):
        """
        Handles 401 Unauthorized errors.

        Args:
            error (HTTPException): The HTTP exception raised.

        Returns:
            Response: The JSON response with error details.
        """
        response = jsonify({'error': 'Unauthorized', 'message': str(error)})
        response.status_code = 401
        return response

    @bp.errorhandler(403)
    def forbidden(error):
        """
        Handles 403 Forbidden errors.

        Args:
            error (HTTPException): The HTTP exception raised.

        Returns:
            Response: The JSON response with error details.
        """
        response = jsonify({'error': 'Forbidden', 'message': str(error)})
        response.status_code = 403
        return response

    @bp.errorhandler(404)
    def not_found(error):
        """
        Handles 404 Not Found errors.

        Args:
            error (HTTPException): The HTTP exception raised.

        Returns:
            Response: The JSON response with error details.
        """
        response = jsonify({'error': 'Not Found', 'message': str(error)})
        response.status_code = 404
        return response

    @bp.errorhandler(500)
    def internal_server_error(error):
        """
        Handles 500 Internal Server Error errors.

        Args:
            error (HTTPException): The HTTP exception raised.

        Returns:
            Response: The JSON response with error details.
        """
        response = jsonify({'error': 'Internal Server Error', 'message': str(error)})
        response.status_code = 500
        return response
   
    @bp.errorhandler(AuthError)
    def handle_auth_error(error):
        """
        Handles authentication errors raised by Auth0.

        Args:
            ex (AuthError): The authentication error raised.

        Returns:
            Response: The JSON response with error details.
        """
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response
