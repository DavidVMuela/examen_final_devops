import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test que la página principal carga correctamente"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'CI/CD Flask + IA' in response.data

def test_health_endpoint(client):
    """Test del endpoint de salud"""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'
    assert json_data['version'] == '1.0.5'

def test_chat_endpoint_without_prompt(client):
    """Test del endpoint de chat sin prompt"""
    response = client.post('/api/chat', json={})
    assert response.status_code == 400

def test_chat_endpoint_with_prompt(client):
    """Test del endpoint de chat con prompt (modo demo)"""
    response = client.post('/api/chat', json={'prompt': 'Hola'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'response' in json_data

def test_version_in_page(client):
    """Test que la versión 1.0.5 aparece en la página"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'1.0.5' in response.data