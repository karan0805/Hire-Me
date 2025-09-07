import pytest
from unittest.mock import patch
from tkinter import Tk
from app.modules import login


@pytest.fixture
def root():
    return Tk()


@pytest.fixture
def mock_login_widgets():
    with (
        patch("app.modules.login.email", create=True) as mock_email,
        patch("app.modules.login.pwd", create=True) as mock_pwd,
    ):
        yield mock_email, mock_pwd


def test_submit_success_recruiter(
    mock_db_connection, root, mock_login_widgets
):
    mock_email, mock_pwd = mock_login_widgets
    mock_email.get.return_value = "recruiter@example.com"
    mock_pwd.get.return_value = "password"

    mock_db_connection.fetchall.side_effect = [
        [("recruiter@example.com", "password")],
        [("recruiter",)],
    ]

    with (
        patch("app.modules.recruiter.rec") as mock_rec_ui,
        patch("app.modules.login.f1", create=True) as mock_frame,
    ):
        login.submit(root)

        mock_rec_ui.assert_called_once_with(root, "recruiter@example.com")
        mock_frame.destroy.assert_called_once()


def test_submit_success_client(mock_db_connection, root, mock_login_widgets):
    mock_email, mock_pwd = mock_login_widgets
    mock_email.get.return_value = "client@example.com"
    mock_pwd.get.return_value = "password"

    mock_db_connection.fetchall.side_effect = [
        [("client@example.com", "password")],
        [("client",)],
    ]

    with (
        patch("app.modules.client.cli") as mock_cli_ui,
        patch("app.modules.login.f1", create=True) as mock_frame,
    ):
        login.submit(root)
        mock_cli_ui.assert_called_once_with(root, "client@example.com")
        mock_frame.destroy.assert_called_once()


def test_submit_invalid_credentials(
    mock_db_connection, root, mock_login_widgets
):
    mock_email, mock_pwd = mock_login_widgets
    mock_email.get.return_value = "user@example.com"
    mock_pwd.get.return_value = "wrong_password"

    mock_db_connection.fetchall.return_value = [
        ("user@example.com", "correct_password")
    ]

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        login.submit(root)
        mock_showinfo.assert_called_with("Alert!", "Invalid Credentials")


def test_submit_unregistered_email(
    mock_db_connection, root, mock_login_widgets
):
    mock_email, mock_pwd = mock_login_widgets
    mock_email.get.return_value = "unregistered@example.com"
    mock_pwd.get.return_value = "password"

    mock_db_connection.fetchall.return_value = []

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        login.submit(root)
        mock_showinfo.assert_called_with(
            "Alert!", "Email is not registered, Please register"
        )


def test_submit_empty_fields(root, mock_login_widgets):
    mock_email, mock_pwd = mock_login_widgets
    mock_email.get.return_value = ""
    mock_pwd.get.return_value = ""

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        login.submit(root)
        mock_showinfo.assert_called_with(
            "Alert!", "Please Enter both Email and Password"
        )
