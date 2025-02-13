"""
This module defines the API routes for the application.
"""

from flask import Blueprint

from controllers.auction_controller import auction_bp
from controllers.bid_controller import bid_bp
from controllers.type_controller import type_bp
from controllers.category_controller import category_bp
from controllers.review_controller import review_bp

routes = Blueprint('routes', __name__)

# Blueprints
routes.register_blueprint(auction_bp)
routes.register_blueprint(bid_bp)
routes.register_blueprint(type_bp)
routes.register_blueprint(category_bp)
routes.register_blueprint(review_bp)