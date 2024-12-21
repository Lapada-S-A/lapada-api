"""
This module defines the API routes for the application.
"""

from flask import Blueprint

from controllers.auction_controller import auction_bp
from controllers.bid_controller import bid_bp

routes = Blueprint('routes', __name__)

# Blueprints
routes.register_blueprint(auction_bp)
routes.register_blueprint(bid_bp)
