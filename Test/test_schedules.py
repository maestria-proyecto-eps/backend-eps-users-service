# import pytest
# from fastapi.testclient import TestClient
# from main import app
# from sqlalchemy import text
# from db.session import SessionLocal
# from datetime import time
#
# client = TestClient(app)
#
# # 1. Test: Crear horario correctamente
# def test_create_schedule():
#     db = SessionLocal()
#     db.execute(text("TRUNCATE TABLE horarios, medicos RESTART IDENTITY CASCADE;"))
#     db.commit()
#
#     # 2. CREAR AL MÉDICO PRIMERO (Necesario para que exista el id_medico: 1)
#     # Usa el id_usuario 1 que creamos en la tabla fantasma
#     medico_payload = {
#         "id_usuario": 1,
#         "nombres": "Medico",
#         "apellidos": "Horario",
#         "num_licencia": 999888,
#         "id_especialidad": 1,
#         "estado": 1
#     }
#     client.post("/api/doctors/", json=medico_payload)
#
#     # 3. CREAR EL HORARIO
#     payload = {
#         "id_medico": 1,
#         "dia_semana": "Lunes",
#         "hora_inicio": "08:00:00",
#         "hora_fin": "10:00:00",
#         "duracion_slot_minutos": 30
#     }
#     response = client.post("/api/schedules/", json=payload)
#
#     db.close()
#     assert response.status_code == 200
#
# # 2. Test: Validar Solapamiento (Debe fallar con 400)
# def test_create_schedule_overlap():
#     # Intentamos crear un horario que choca con el anterior (08:00 - 10:00)
#     payload_conflictivo = {
#         "id_medico": 1,
#         "dia_semana": "Lunes",
#         "hora_inicio": "09:00:00",
#         "hora_fin": "11:00:00",
#         "duracion_slot_minutos": 30
#     }
#     response = client.post("/api/schedules/", json=payload_conflictivo)
#     assert response.status_code == 400
#     assert "Conflicto" in response.json()["detail"]
#
# # 3. Test: Generar Slots
# def test_generate_slots():
#     # Buscamos slots para el médico 1 en un lunes (2026-03-02 es Lunes)
#     # Nota: Asegúrate que el médico 1 tenga horario el Lunes según el test anterior
#     response = client.get("/api/schedules/generate-slots/1?fecha=2026-03-02")
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#
#     # Si el horario es de 08:00 a 10:00 con slots de 30 min, debería haber 4 slots
#     # 08:00, 08:30, 09:00, 09:30
#     assert len(data) == 4
#     assert data[0]["hora_inicio"] == "08:00:00"
#
# # 4. Test: Horario no encontrado (Día que no trabaja)
# def test_generate_slots_not_found():
#     # 2026-03-01 es Domingo, el doctor no tiene horario ese día
#     response = client.get("/api/schedules/generate-slots/1?fecha=2026-03-01")
#     assert response.status_code == 404