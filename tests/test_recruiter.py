import pytest
from unittest.mock import MagicMock, patch
from tkinter import Tk
from app.modules import recruiter


@pytest.fixture
def root():
    return Tk()


def test_get_details(mock_db_connection):
    mock_db_connection.fetchall.return_value = [
        ("Test Recruiter", "Test Company", "F", 1)
    ]
    recruiter.get_details("recruiter@example.com")
    assert recruiter.name == "Test Recruiter"
    assert recruiter.company == "Test Company"
    assert recruiter.gen == "F"
    assert recruiter.recid == 1


def test_submit_job_success(mock_db_connection):
    recruiter.role = MagicMock()
    recruiter.jtype = MagicMock()
    recruiter.qual = MagicMock()
    recruiter.exp = MagicMock()
    recruiter.sal = MagicMock()

    recruiter.role.get.return_value = "Python Developer"
    recruiter.jtype.get.return_value = "FullTime"
    recruiter.qual.get.return_value = "Computer Science Degree"
    recruiter.exp.get.return_value = "3"
    recruiter.sal.get.return_value = "7000"

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        recruiter.submit_job()

        mock_db_connection.execute.assert_called_once()
        mock_showinfo.assert_called_with(
            "SUCCESS!", "You have successfully created a Job"
        )


def test_submit_job_missing_fields():
    recruiter.role = MagicMock()
    recruiter.jtype = MagicMock()
    recruiter.qual = MagicMock()
    recruiter.exp = MagicMock()
    recruiter.sal = MagicMock()

    recruiter.role.get.return_value = ""
    recruiter.jtype.get.return_value = "FullTime"
    recruiter.qual.get.return_value = "CS"
    recruiter.exp.get.return_value = "1"
    recruiter.sal.get.return_value = ""

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        recruiter.submit_job()
        mock_showinfo.assert_called_with(
            "ALERT!", "ALL FIELDS ARE MUST BE FILLED"
        )


def test_submit_job_type_not_selected():
    recruiter.role = MagicMock()
    recruiter.jtype = MagicMock()
    recruiter.qual = MagicMock()
    recruiter.exp = MagicMock()
    recruiter.sal = MagicMock()

    recruiter.role.get.return_value = "Developer"
    recruiter.jtype.get.return_value = "Select"
    recruiter.qual.get.return_value = "CS"
    recruiter.exp.get.return_value = "1"
    recruiter.sal.get.return_value = "1000"

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        recruiter.submit_job()
        mock_showinfo.assert_called_with("ALERT!", "Please provide Job Type")


def test_deletjob(mock_db_connection):
    table = MagicMock()
    table.focus.return_value = "item1"
    table.item.return_value = (1, "Developer")

    with (
        patch("tkinter.messagebox.showinfo") as mock_showinfo,
        patch("app.modules.recruiter.posted") as mock_posted,
    ):
        recruiter.deletjob(table)

        assert mock_db_connection.execute.call_count == 2
        mock_showinfo.assert_called_with("Thanks", "Your Job has been Deleted")
        mock_posted.assert_called_once()


def test_show_all(mock_db_connection):
    table = MagicMock()
    mock_db_connection.fetchall.return_value = [
        (1, 101, "Dev", "FullTime", "BSc", 2, 5000),
    ]
    recruiter.recid = 1

    recruiter.show_all(table)

    assert table.insert.call_count == 1
    table.insert.assert_called_with(
        "", 0, text="", values=(101, "Dev", "FullTime", "BSc", 2, 5000)
    )


def test_show_applicants(mock_db_connection):
    table = MagicMock()
    mock_db_connection.fetchall.return_value = [
        (
            "Dev",
            "John Doe",
            "john@mail.com",
            30,
            "City A",
            "M",
            5,
            "Python",
            "MSc",
        ),
    ]
    recruiter.recid = 1

    recruiter.show_applicants(table)

    assert table.insert.call_count == 1
    table.insert.assert_called_with(
        "",
        0,
        text="",
        values=(
            "Dev",
            "John Doe",
            "john@mail.com",
            30,
            "City A",
            "M",
            5,
            "Python",
            "MSc",
        ),
    )


def test_sort_applicants(mock_db_connection):
    table = MagicMock()
    recruiter.recid = 1

    with patch("app.modules.recruiter.search_d", create=True) as mock_search_d:
        mock_search_d.get.return_value = "CName"

        recruiter.sort_applicants(table)

        table.delete.assert_called_once_with(*table.get_children())

        mock_db_connection.execute.assert_called_with(
            "SELECT job.JobRole, client.CName, client.CEmail, client.CAge,"
            "client.CLocation, client.CGender, client.CExp, "
            "client.CSkills, client.CQualification FROM application "
            "JOIN client ON application.cid=client.CID JOIN job ON "
            f"job.jid=application.jid where job.rid={recruiter.recid} order "
            "by CName"
        )
