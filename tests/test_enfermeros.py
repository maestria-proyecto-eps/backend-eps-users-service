"""Pruebas unitarias para el router de enfermeros"""

def test_get_enfermeros_success(client):
    """Prueba obtener lista de enfermeros vacía"""
    response = client.get("/nurses/")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)

def test_create_enfermero_success(client, test_usuario):
    """Prueba crear un nuevo enfermero"""
    data = {
        "nombres": "Laura",
        "apellidos": "Gomez",
        "estado": 1,
        "id_usuario": 2
    }
    response = client.post("/nurses/", json=data)
    assert response.status_code == 201
    assert response.json()["hasError"] == False
    assert response.json()["data"]["nombres"] == data["nombres"]

def test_create_enfermero_usuario_inexistente(client):
    """Prueba crear enfermero con usuario inexistente"""
    data = {
        "nombres": "Pedro",
        "apellidos": "Lopez",
        "estado": 1,
        "id_usuario": 9999
    }
    response = client.post("/nurses/", json=data)
    assert response.status_code == 400  # llega al service
    assert response.json()["hasError"] == True

def test_update_enfermero_success(client):
    """Prueba actualizar un enfermero existente"""
    data = {
        "nombres": "Laura Actualizada",
        "estado": 0
    }
    response = client.put("/nurses/2", json=data)
    assert response.status_code == 200
    assert response.json()["hasError"] == False
    assert response.json()["data"]["nombres"] == data["nombres"]

def test_update_enfermero_not_found(client):
    """Prueba actualizar enfermero con usuario inexistente"""
    data = {
        "nombres": "Inexistente"
    }
    response = client.put("/nurses/9999", json=data)
    assert response.status_code == 400
    assert response.json()["hasError"] == True
