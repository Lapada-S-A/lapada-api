from db import db
from models.review import Review
from datetime import datetime
from sqlalchemy import func


class ReviewService:
    """
    Service class for handling review-related operations.
    """

    @staticmethod
    def create_review(data):
        """
        Create a new review.

        Args:
            data (dict): Data containing review details.

        Returns:
            Review: The created review object.
        """
        review = Review(
            rate=data["rate"],
            comment=data.get("comment"),
            buyer_id=data["buyer_id"],
            seller_id=data["seller_id"],
            auction_id=data["auction_id"],
            created_at=datetime.utcnow(),
        )

        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def get_all_reviews():
        """
        Retrieve all reviews from the database.

        Returns:
            List[Review]: A list of all reviews.
        """
        return Review.query.all()

    @staticmethod
    def get_review_by_id(review_id):
        """
        Retrieve a specific review by ID.

        Args:
            review_id (int): The ID of the review.

        Returns:
            Review or None: The review object if found, otherwise None.
        """
        return Review.query.get(review_id)

    @staticmethod
    def update_review(review_id, data):
        """
        Update an existing review.

        Args:
            review_id (int): The ID of the review to update.
            data (dict): The updated data.

        Returns:
            Review or None: The updated review object if found, otherwise None.
        """
        review = Review.query.get(review_id)
        if not review:
            return None

        review.rate = data.get("rate", review.rate)
        review.comment = data.get("comment", review.comment)

        db.session.commit()
        return review

    @staticmethod
    def delete_review(review_id):
        """
        Delete a review by ID.

        Args:
            review_id (int): The ID of the review to delete.

        Returns:
            bool: True if deleted, False otherwise.
        """
        review = Review.query.get(review_id)
        if not review:
            return False

        db.session.delete(review)
        db.session.commit()
        return True

    @staticmethod
    def get_reviews_by_seller(seller_id):
        """
        Get all reviews received by a specific seller.

        Args:
            seller_id (int): The ID of the seller.

        Returns:
            List[Review]: List of reviews received by the seller.
        """
        return Review.query.filter_by(seller_id=seller_id).all()

    @staticmethod
    def get_reviews_by_buyer(buyer_id):
        """
        Get all reviews made by a specific buyer.

        Args:
            buyer_id (int): The ID of the buyer.

        Returns:
            List[Review]: List of reviews made by the buyer.
        """
        return Review.query.filter_by(buyer_id=buyer_id).all()
    
    @staticmethod
    def get_review_by_auction(auction_id):
        """
        Get review of a specific auction.

        Args:
            auction_id (int): The ID of auction.

        Returns:
            Review: Review of the auction.
        """
        return Review.query.filter_by(auction_id=auction_id).all()

    @staticmethod
    def get_seller_average_rating(seller_id):
        """
        Calculate the average rating of a seller based on received reviews.

        Args:
            seller_id (int): The ID of the seller.

        Returns:
            float or None: The average rating, or None if no reviews exist.
        """
        avg_rating = (
            db.session.query(func.avg(Review.rate))
            .filter_by(seller_id=seller_id)
            .scalar()
        )
        return round(avg_rating, 2) if avg_rating is not None else None