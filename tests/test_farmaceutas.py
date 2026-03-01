"""Pruebas unitarias para el router de farmaceutas"""

def test_get_farmaceutas_success(client):
    """Prueba obtener lista de farmaceutas vacía"""
    response = client.get("/pharmacists/")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)

def test_create_farmaceuta_success(client):
    """Prueba crear un nuevo farmaceuta"""
    data = {
        "nombres": "Carlos",
        "apellidos": "Ramirez",
        "estado": 1,
        "id_usuario": 2
    }
    response = client.post("/pharmacists/", json=data)
    assert response.status_code == 201
    assert response.json()["hasError"] == False
    assert response.json()["data"]["nombres"] == data["nombres"]

def test_create_farmaceuta_usuario_inexistente(client):
    """Prueba crear farmaceuta con usuario inexistente"""
    data = {
        "nombres": "Ana",
        "apellidos": "Torres",
        "estado": 1,
        "id_usuario": 9999
    }
    response = client.post("/pharmacists/", json=data)
    assert response.status_code == 400
    assert response.json()["hasError"] == True

def test_update_farmaceuta_success(client):
    """Prueba actualizar un farmaceuta existente"""
    data = {
        "nombres": "Carlos Actualizado",
        "estado": 0
    }
    response = client.put("/pharmacists/2", json=data)
    assert response.status_code == 200
    assert response.json()["hasError"] == False
    assert response.json()["data"]["nombres"] == data["nombres"]

def test_update_farmaceuta_not_found(client):
    """Prueba actualizar farmaceuta con usuario inexistente"""
    data = {
        "nombres": "Inexistente"
    }
    response = client.put("/pharmacists/9999", json=data)
    assert response.status_code == 400
    assert response.json()["hasError"] == True
