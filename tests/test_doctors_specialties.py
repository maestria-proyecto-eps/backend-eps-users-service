from models.Usuario import Usuario
from models.doctor import Doctor
from models.specialty import Specialty


def _ensure_specialty(db, id_especialidad: int, nombre: str, requiere_remision: bool = False):
    specialty = db.query(Specialty).filter(Specialty.id_especialidad == id_especialidad).first()
    if specialty is None:
        specialty = Specialty(
            id_especialidad=id_especialidad,
            nombre_especialidad=nombre,
            requiere_remision=requiere_remision,
        )
        db.add(specialty)
        db.commit()
        db.refresh(specialty)
    return specialty


def _ensure_user(db, id_usuario: int, id_rol: int = 1):
    user = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if user is None:
        user = Usuario(
            id_usuario=id_usuario,
            num_documento=900000000 + id_usuario,
            password="abc123456",
            id_rol=id_rol,
            estado=1,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def _ensure_doctor(db, id_medico: int, id_usuario: int, id_especialidad: int, num_licencia: int):
    doctor = db.query(Doctor).filter(Doctor.id_medico == id_medico).first()
    if doctor is None:
        doctor = Doctor(
            id_medico=id_medico,
            nombres="Doctor",
            apellidos="Base",
            num_licencia=num_licencia,
            id_especialidad=id_especialidad,
            id_usuario=id_usuario,
            estado=1,
        )
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
    return doctor


def test_get_specialties_success(client, db_session):
    _ensure_specialty(db_session, 101, "Medicina General")
    _ensure_specialty(db_session, 102, "Pediatria", True)

    response = client.get("/api/specialties/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["nombre_especialidad"] == "Medicina General" for item in data)


def test_create_doctor_success(client, db_session):
    _ensure_specialty(db_session, 103, "Cardiologia")
    _ensure_user(db_session, 103)

    payload = {
        "id_medico": 700001,
        "nombres": "Laura",
        "apellidos": "Suarez",
        "num_licencia": 880001,
        "id_especialidad": 103,
        "id_usuario": 103,
        "estado": 1,
    }

    response = client.post("/api/doctors/", json=payload)
    assert response.status_code == 201
    assert response.json()["id_medico"] == payload["id_medico"]
    assert response.json()["num_licencia"] == payload["num_licencia"]


def test_create_doctor_invalid_specialty(client, db_session):
    _ensure_user(db_session, 104)

    payload = {
        "id_medico": 700002,
        "nombres": "Mario",
        "apellidos": "Lopez",
        "num_licencia": 880002,
        "id_especialidad": 9999,
        "id_usuario": 104,
        "estado": 1,
    }

    response = client.post("/api/doctors/", json=payload)
    assert response.status_code == 400
    assert "no existe" in response.json()["detail"]


def test_get_doctors_by_specialty_success(client, db_session):
    _ensure_specialty(db_session, 105, "Neurologia")
    _ensure_specialty(db_session, 106, "Ortopedia")
    _ensure_user(db_session, 105)
    _ensure_user(db_session, 106)
    _ensure_doctor(db_session, 700003, 105, 105, 880003)
    _ensure_doctor(db_session, 700004, 106, 106, 880004)

    response = client.get("/api/doctors/by-specialty/?id_especialidad=105")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(item["id_especialidad"] == 105 for item in data)


def test_update_doctor_specialty_success(client, db_session):
    _ensure_specialty(db_session, 107, "Dermatologia")
    _ensure_specialty(db_session, 108, "Psiquiatria")
    _ensure_user(db_session, 107)
    _ensure_doctor(db_session, 700005, 107, 107, 880005)

    response = client.put("/api/doctors/700005/specialty", json={"id_especialidad": 108})
    assert response.status_code == 200
    assert response.json()["id_especialidad"] == 108


def test_update_doctor_specialty_not_found(client):
    response = client.put("/api/doctors/999999/specialty", json={"id_especialidad": 1})
    assert response.status_code == 404


def test_update_doctor_specialty_invalid_specialty(client, db_session):
    _ensure_specialty(db_session, 109, "Ginecologia")
    _ensure_user(db_session, 109)
    _ensure_doctor(db_session, 700006, 109, 109, 880006)

    response = client.put("/api/doctors/700006/specialty", json={"id_especialidad": 9999})
    assert response.status_code == 400
    assert "no existe" in response.json()["detail"]
