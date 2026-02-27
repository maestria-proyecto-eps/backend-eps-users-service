
"""Pruebas unitarias para el router de usuarios"""

def test_get_users_success(client):
    """Prueba obtener lista de usuarios"""
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json()["data"]["data"], list)
    
def test_create_user_success(client,test_rol):
    """Prueba crear un nuevo usuario"""
    user_data = {
        "num_documento": 123456,
        "password": "abc123456",
        "id_rol": 1
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["data"]["num_documento"] == user_data["num_documento"]

def test_get_user_by_id_success(client):
    """Prueba obtener usuario por ID"""
    user_id = 1
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id_usuario"] == user_id

def test_get_user_by_id_not_found(client):
    """Prueba obtener usuario con ID inexistente"""
    response = client.get("/users/9999")
    assert response.status_code == 400

def test_create_user_invalid_data(client):
    """Prueba crear usuario con datos inválidos"""
    user_data = {
        "num_documento": 123456,
        "password": "abc123456",
        "id_rol": 9999
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 400

def test_update_user_success(client):
    """Prueba actualizar un usuario"""
    user_id = 1
    user_data = {
        "num_documento": 456789,
        "id_rol": 1
    }
    response = client.put(f"/users/{user_id}", json=user_data)
    assert response.status_code == 200
    assert response.json()["data"]["num_documento"] == user_data["num_documento"]

def test_update_user_not_found(client):
    """Prueba actualizar usuario inexistente"""
    user_data = {
        "num_documento": 1234567890,
        "id_rol": 2
    }
    response = client.put("/users/9999", json=user_data)
    assert response.status_code == 400

def test_delete_user_success(client):
    """Prueba eliminar un usuario"""
    user_id = 1
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

def test_delete_user_not_found(client):
    """Prueba eliminar usuario inexistente"""
    response = client.delete("/users/9999")
    assert response.status_code == 400