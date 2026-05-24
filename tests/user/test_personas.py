"""Pruebas unitarias para el router de personas"""


def test_get_personas_success(client):
    """Prueba obtener lista de personas vacía"""
    response = client.get("/api/persons/")
    assert response.status_code == 200
    assert isinstance(response.json()["data"]["data"], list)


def test_create_persona_success(client):
    """Prueba crear una nueva persona"""
    data = {
        "num_documento": 987654321,
        "nombres": "Carlos",
        "apellidos": "Ramirez",
    }
    response = client.post("/api/persons/", json=data)
    assert response.status_code == 201
    assert response.json()["hasError"] == False
    assert response.json()["data"]["nombres"] == data["nombres"]


def test_create_persona_documento_duplicado(client):
    """Prueba crear persona con documento ya existente"""
    data = {
        "num_documento": 987654321,
        "nombres": "Jaime",
        "apellidos": "Ortiz",
    }
    response = client.post("/api/persons/", json=data)
    assert response.status_code == 400
    assert response.json()["hasError"] == True


def test_get_persona_by_documento_success(client):
    """Prueba obtener persona por num_documento"""
    response = client.get("/api/persons/987654321")
    assert response.status_code == 200
    assert response.json()["data"]["num_documento"] == 987654321


def test_get_persona_by_documento_not_found(client):
    """Prueba obtener persona con documento inexistente"""
    response = client.get("/api/persons/9999999")
    assert response.status_code == 400
    assert response.json()["hasError"] == True


def test_update_persona_success(client):
    """Prueba actualizar una persona existente"""
    data = {"nombres": "Carlos Actualizado"}
    response = client.put("/api/persons/987654321", json=data)
    assert response.status_code == 200
    assert response.json()["data"]["nombres"] == data["nombres"]


def test_update_persona_not_found(client):
    """Prueba actualizar persona inexistente"""
    data = {"nombres": "Inexistente"}
    response = client.put("/api/persons/9999999", json=data)
    assert response.status_code == 400
    assert response.json()["hasError"] == True