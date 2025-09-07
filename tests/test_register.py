import pytest
from unittest.mock import MagicMock, patch
from tkinter import Tk
from app.modules import register


@pytest.fixture
def root():
    return Tk()


@pytest.fixture
def mock_register_widgets():
    widget_names = [
        "name",
        "email",
        "pwd",
        "cpwd",
        "gender",
        "company",
        "loc",
        "age",
        "workxp",
        "qualification",
        "skills",
    ]

    with patch.multiple(
        "app.modules.register",
        create=True,
        **{name: MagicMock() for name in widget_names},
    ):
        register.gender.get.return_value = "M"
        yield


def test_recruiter_check_success(
    mock_db_connection, root, mock_register_widgets
):
    register.name.get.return_value = "Test Recruiter"
    register.email.get.return_value = "new@recruiter.com"
    register.pwd.get.return_value = "password123"
    register.cpwd.get.return_value = "password123"

    mock_db_connection.fetchall.return_value = []

    with patch(
        "app.modules.register.recruit_complete"
    ) as mock_recruit_complete:
        register.recruiter_check(root)
        mock_recruit_complete.assert_called_once_with(root)


def test_recruiter_check_email_exists(
    mock_db_connection, root, mock_register_widgets
):
    register.name.get.return_value = "Test Recruiter"
    register.email.get.return_value = "exists@recruiter.com"
    register.pwd.get.return_value = "password123"
    register.cpwd.get.return_value = "password123"

    mock_db_connection.fetchall.return_value = [("exists@recruiter.com",)]

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        register.recruiter_check(root)
        mock_showinfo.assert_called_with("ALERT!", "EMAIL ALREADY REGISTERED")


def test_recruiter_check_password_mismatch(root, mock_register_widgets):
    register.name.get.return_value = "Test Recruiter"
    register.email.get.return_value = "new@recruiter.com"
    register.pwd.get.return_value = "password123"
    register.cpwd.get.return_value = "password456"

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        register.recruiter_check(root)
        mock_showinfo.assert_called_with("ALERT!", "PASSWORDS DO NOT MATCH")


def test_recruiter_submit_success(
    mock_db_connection, root, mock_register_widgets
):
    register.company.get.return_value = "Test Corp"
    register.loc.get.return_value = "Test City"

    with (
        patch("app.modules.register.logi") as mock_logi,
        patch("tkinter.messagebox.showinfo") as mock_showinfo,
    ):
        register.recruiter_submit(root)

        assert mock_db_connection.execute.call_count == 2
        mock_showinfo.assert_called_with("SUCCESS!", "Registration Successful")
        mock_logi.assert_called_once_with(root)


def test_client_check_success(mock_db_connection, root, mock_register_widgets):
    register.name.get.return_value = "Test Client"
    register.email.get.return_value = "new@client.com"
    register.pwd.get.return_value = "password123"
    register.cpwd.get.return_value = "password123"

    mock_db_connection.fetchall.return_value = []

    with patch("app.modules.register.client_complete") as mock_client_complete:
        register.client_check(root)
        mock_client_complete.assert_called_once_with(root)


def test_client_submit_success(
    mock_db_connection, root, mock_register_widgets
):
    register.age.get.return_value = "30"
    register.loc.get.return_value = "Test Ville"
    register.workxp.get.return_value = "5"
    register.qualification.get.return_value = "PhD"
    register.skills.get.return_value = "Testing, Mocking"

    with (
        patch("app.modules.register.logi") as mock_logi,
        patch("tkinter.messagebox.showinfo") as mock_showinfo,
    ):
        register.client_submit(root)

        assert (
            mock_db_connection.execute.call_count == 2
        )  # Deve inserir em 'users' e 'client'
        mock_showinfo.assert_called_with("SUCCESS!", "Registration Successful")
        mock_logi.assert_called_once_with(root)


def test_client_submit_missing_fields(root, mock_register_widgets):
    register.age.get.return_value = "30"
    register.loc.get.return_value = ""
    register.workxp.get.return_value = "5"

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        register.client_submit(root)
        mock_showinfo.assert_called_with(
            "ALERT!", "ALL FIELDS ARE MUST BE FILLED"
        )
