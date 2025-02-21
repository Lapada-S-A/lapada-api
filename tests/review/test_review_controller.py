import pytest
from app import app
from db import db
from models.review import Review
from services.review_service import ReviewService

@pytest.fixture(scope='module')
def init_database():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

        review = Review(rate=5, buyer_id=1, seller_id=1, comment="Great service!")
        db.session.add(review)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

def test_create_review(init_database):
    with app.app_context():
        db = init_database
        review_data = {"rate": 4, "buyer_id": 2, "seller_id": 1, "comment": "Good service."}
        response = app.test_client().post('/review/create', json=review_data)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == "Review created successfully"
        assert data['review']['rate'] == 4

def test_create_review_missing_fields(init_database):
    with app.app_context():
        db = init_database
        review_data = {"rate": 4, "buyer_id": 2}
        response = app.test_client().post('/review/create', json=review_data)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == "Missing required fields"

def test_get_all_reviews(init_database):
    with app.app_context():
        db = init_database
        response = app.test_client().get('/review/list')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0

def test_get_review_by_id(init_database):
    with app.app_context():
        db = init_database
        review = Review.query.first()
        response = app.test_client().get(f'/review/list/{review.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['rate'] == review.rate

def test_get_review_by_id_not_found(init_database):
    with app.app_context():
        db = init_database
        response = app.test_client().get('/review/list/999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == "Review not found"

def test_update_review(init_database):
    with app.app_context():
        db = init_database
        review = Review.query.first()
        update_data = {"rate": 3, "comment": "Updated comment."}
        response = app.test_client().put(f'/review/update/{review.id}', json=update_data)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == "Review updated successfully"
        assert data['review']['rate'] == 3
        assert data['review']['comment'] == "Updated comment."

def test_update_review_not_found(init_database):
    with app.app_context():
        db = init_database
        update_data = {"rate": 3, "comment": "Updated comment."}
        response = app.test_client().put('/review/update/999', json=update_data)
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == "Review not found"

def test_delete_review(init_database):
    with app.app_context():
        db = init_database
        review = Review.query.first()
        response = app.test_client().delete(f'/review/delete/{review.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == "Review deleted successfully"

def test_delete_review_not_found(init_database):
    with app.app_context():
        db = init_database
        response = app.test_client().delete('/review/delete/999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == "Review not found"

def test_get_reviews_by_seller(init_database):
    with app.app_context():
        db = init_database
        seller_id = 1
        response = app.test_client().get(f'/review/list/seller/{seller_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0

def test_get_reviews_by_buyer(init_database):
    with app.app_context():
        db = init_database
        buyer_id = 1
        response = app.test_client().get(f'/review/list/buyer/{buyer_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
