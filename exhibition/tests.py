import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Breed, Kitten

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def breed():
    return Breed.objects.create(name='Siamese')

@pytest.fixture
def kitten(user, breed):
    return Kitten.objects.create(breed=breed, color='White', age=3, description='Cute kitten', owner=user)

@pytest.mark.django_db
def test_get_breeds(api_client, breed):
    response = api_client.get('/api/breeds/')
    assert response.status_code == 200
    assert response.data[0]['name'] == 'Siamese'

@pytest.mark.django_db
def test_create_kitten(api_client, user, breed):
    api_client.force_authenticate(user=user)
    data = {
        'breed': breed.id,
        'color': 'Black',
        'age': 2,
        'description': 'Playful kitten',
    }
    response = api_client.post('/api/kittens/', data)
    assert response.status_code == 201
    assert response.data['owner'] == 'testuser'

@pytest.mark.django_db
def test_rate_kitten(api_client, user, kitten):
    api_client.force_authenticate(user=user)
    data = {'score': 5}
    response = api_client.post(f'/api/kittens/{kitten.id}/rate/', data, format='json')
    assert response.status_code == 201
    assert response.data['score'] == 5
