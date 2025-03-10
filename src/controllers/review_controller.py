from flask import Blueprint, request, jsonify
from services.review_service import ReviewService

from models.review import Review

review_bp = Blueprint("review", __name__, url_prefix="/review")


@review_bp.route("/create", methods=["POST"])
def create_review():
    """
    Create a new review.
    """
    data = request.get_json()
    required_fields = ["rate", "buyer_id", "seller_id"]

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    review = ReviewService.create_review(data)
    return (
        jsonify({"message": "Review created successfully", "review": review.to_dict()}),
        201,
    )


@review_bp.route("/list", methods=["GET"])
def get_all_reviews():
    """
    Get all reviews.
    """
    reviews = ReviewService.get_all_reviews()
    return jsonify([review.to_dict() for review in reviews]), 200


@review_bp.route("/list/<int:review_id>", methods=["GET"])
def get_review_by_id(review_id):
    """
    Get a single review by ID.
    """
    review = ReviewService.get_review_by_id(review_id)
    if not review:
        return jsonify({"message": "Review not found"}), 404

    return jsonify(review.to_dict()), 200


@review_bp.route("/update/<int:review_id>", methods=["PUT"])
def update_review(review_id):
    """
    Update an existing review.
    """
    data = request.get_json()
    review = ReviewService.update_review(review_id, data)
    if not review:
        return jsonify({"message": "Review not found"}), 404

    return (
        jsonify({"message": "Review updated successfully", "review": review.to_dict()}),
        200,
    )


@review_bp.route("/delete/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Delete a review.
    """
    success = ReviewService.delete_review(review_id)
    if not success:
        return jsonify({"message": "Review not found"}), 404

    return jsonify({"message": "Review deleted successfully"}), 200


@review_bp.route("/list/seller/<int:seller_id>", methods=["GET"])
def get_reviews_by_seller(seller_id):
    """
    Get all reviews received by a seller.
    """
    reviews = ReviewService.get_reviews_by_seller(seller_id)
    return jsonify([review.to_dict() for review in reviews]), 200


@review_bp.route("/list/buyer/<int:buyer_id>", methods=["GET"])
def get_reviews_by_buyer(buyer_id):
    """
    Get all reviews made by a buyer.
    """
    reviews = ReviewService.get_reviews_by_buyer(buyer_id)
    return jsonify([review.to_dict() for review in reviews]), 200


@review_bp.route("/list/seller/<int:seller_id>/rating", methods=["GET"])
def get_seller_average_rating(seller_id):
    """
    Get the average rating of a seller.
    """
    avg_rating = ReviewService.get_seller_average_rating(seller_id)

    if avg_rating is None:
        return (
            jsonify({"message": "Seller has no reviews yet", "average_rating": None}),
            204,
        )

    return jsonify({"seller_id": seller_id, "average_rating": avg_rating}), 200
