import pytest 
import sqlite3
from usuario_sistema import adicionar_usuario, buscar_usuario

@pytest.fixture
def db_connection():
    """
    Fixture configura uma conexão com um banco de dados SQLite
    temporário e garante a limpeza dos recursos após o teste 
    """
    conn = sqlite3.connect(":memory:")# Cria o banco de dados em mamória 
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE usuarios(
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE 
    )
    """
    )
    conn.commit()
    yield conn, cursor
    conn.close()

@pytest.mark.parametrize(
    "id, nome, email, esperado_nome",
    [
        (1,"Wagner", "wagner@gmail.com", "Wagner"),
        (2,"Emanuelle", "Emanuelleelkhaitib@gmail.com", "Emanuelle"),
        (3,"Matheus", "matheuselkhaitib@gmail.com", "Matheus")
    ]
)
@pytest.mark.unit
def teste_adicionar_usuario(db_connection, id, nome, email, esperado_nome):
    conn, cursor = db_connection
    adicionar_usuario(cursor, id, nome, email)
    resultado = buscar_usuario(cursor, email)

    assert resultado is not None
    assert resultado[1] == esperado_nome
    assert resultado[2] == email

@pytest.mark.integration
def test_buscar_usuario_com_email_inexistente(db_connection):
    conn, cursor = db_connection
    resultado = buscar_usuario (cursor,"naoexistente@example.com")
    assert resultado is None

@pytest.mark.slow
@pytest.mark.integration
def test_adicionar_e_buscar_varios_usuarios(db_connection):
    import time 
    conn,cursor = db_connection

    for i in range(100):
       adicionar_usuario(cursor, i, f"User{i}", f"User{i}@exemplo.com")
       conn.commit()

    time.sleep(2)

    for i in range(100):
        resultado = buscar_usuario(cursor, f"User{i}@exemplo.com")

        assert resultado is not None
        assert resultado[1] == f"User{i}"
        assert resultado[2] == f"User{i}@exemplo.com"
    