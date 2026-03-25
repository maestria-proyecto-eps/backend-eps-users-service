
"""Pruebas unitarias para el router de usuarios"""

def test_get_users_success(client):
    """Prueba obtener lista de usuarios"""
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json()["data"]["data"], list)
    
def test_create_user_success(client, test_persona):
    """Prueba crear un nuevo usuario"""
    user_data = {
        "num_documento": 123456,
        "password": "abc123456",
        "id_rol": 1
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["data"]["num_documento"] == user_data["num_documento"]

def test_get_user_by_id_success(client, test_user):
    """Prueba obtener usuario por ID"""
    user_id = 1
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id_usuario"] == user_id

def test_get_user_by_id_not_found(client):
    """Prueba obtener usuario con ID inexistente"""
    response = client.get("/api/users/9999")
    assert response.status_code == 400

def test_create_user_invalid_data(client):
    """Prueba crear usuario con datos inválidos"""
    user_data = {
        "num_documento": 999999,
        "password": "abc123456",
        "id_rol": 9999
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 400

def test_update_user_success(client,test_user, test_rol):
    """Prueba actualizar un usuario"""
    user_id = 1
    user_data = {
        "id_rol": 1,
        "nombres": "Laura Actualizada",
        "apellidos": "Gomez"
    }
    response = client.put(f"/api/users/{user_id}", json=user_data)
    assert response.status_code == 200
    assert response.json()["data"]["persona"]["nombres"] == user_data["nombres"]

def test_update_user_not_found(client):
    """Prueba actualizar usuario inexistente"""
    user_data = {
        "id_rol": 1
    }
    response = client.put("/api/users/9999", json=user_data)
    assert response.status_code == 400

def test_delete_user_success(client, test_user, test_rol):
    """Prueba soft delete de un usuario"""
    user_id = 1
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

def test_delete_user_not_found(client):
    """Prueba eliminar usuario inexistente"""
    response = client.delete("/api/users/9999")
    assert response.status_code == 400

def test_get_users_filter_by_documento(client, test_user):
    """Prueba filtrar usuarios por num_documento"""
    response = client.get("/api/users?num_documento=123456789")
    assert response.status_code == 200
    assert isinstance(response.json()["data"]["data"], list)


def test_get_users_filter_by_nombre(client, test_user):
    """Prueba filtrar usuarios por nombre"""
    response = client.get("/api/users?nombres=Laura")
    assert response.status_code == 200
    assert isinstance(response.json()["data"]["data"], list)


def test_get_users_filter_by_apellido(client, test_user):
    """Prueba filtrar usuarios por apellido"""
    response = client.get("/api/users?apellidos=Gomez")
    assert response.status_code == 200
    assert isinstance(response.json()["data"]["data"], list)

def test_create_user_persona_not_found(client):
    """Prueba crear usuario cuando la persona no existe"""
    user_data = {
        "num_documento": 99999999,  # documento que no existe en Persona
        "password": "abc123456",
        "id_rol": 1
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 404
    assert response.json()["message"].startswith("Persona no encontrada")