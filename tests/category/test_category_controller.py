import pytest
from app import app
from db import db
from models.category import Category
from services.category_service import CategoryService

@pytest.fixture(scope='module')
def init_database():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

        category = Category(name="Electronics")
        db.session.add(category)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

def test_create_category(init_database):
    with app.app_context():
        db = init_database
        category_data = {"name": "Electronics"}
        response = app.test_client().post('/category/create', json=category_data)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == "Electronics"

def test_create_category_missing_name(init_database):
    with app.app_context():
        db = init_database
        category_data = {}
        response = app.test_client().post('/category/create', json=category_data)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

def test_list_categories(init_database):
    with app.app_context():
        db = init_database
        response = app.test_client().get('/category/list')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0

def test_get_category_by_id(init_database):
    with app.app_context():
        db = init_database
        category = Category.query.first()
        response = app.test_client().get(f'/category/list/{category.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == category.name

def test_get_category_by_id_not_found(init_database):
    with app.app_context():
        db = init_database
        response = app.test_client().get('/category/list/999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data