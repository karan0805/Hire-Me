import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_db_connection():
    with patch(
        "app.utils.database.MySQLConnection._get_conection"
    ) as mock_get_connection:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_get_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        yield mock_cursor
