from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from database import Base
from main import app, get_db

# ========================#
#  CREATE TEST DATABASE  #
# ========================#

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    function to define the database during tests
    :return:
    """
    try:
        test_db = TestingSessionLocal()
        yield test_db
    finally:
        test_db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# ========================#
#          TESTS          #
# ========================#

class TestCreation:
    def test_create_new_comment(self):
        data = {
            "comment": "Ceci est un test"
        }
        target = "Test-1234"
        response = client.post(f"/target/{target}/comments", json=data)

        assert response.status_code == 201

    def test_comment_is_not_in_en_or_fr(self):
        data = {
            "comment": "Soy un test en español"
        }
        target = "Test-1234"
        response = client.post(f"/target/{target}/comments", json=data)

        assert response.status_code == 400
        assert response.json() == {"detail": "comment is empty or not in en-fr"}

    def test_comment_is_empty(self):
        data = {
            "comment": ""
        }
        target = "Test-1234"
        response = client.post(f"/target/{target}/comments", json=data)

        assert response.status_code == 400
        assert response.json() == {"detail": "comment is empty or not in en-fr"}
