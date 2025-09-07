import pytest
from unittest.mock import MagicMock, patch
from tkinter import Tk
from app.modules import client


@pytest.fixture
def root():
    return Tk()


def test_get_details(mock_db_connection):
    mock_db_connection.fetchall.return_value = [
        ("Test Client", "Test Location", "M", 1)
    ]
    client.get_details("test@example.com")
    assert client.name == "Test Client"
    assert client.location == "Test Location"
    assert client.gen == "M"
    assert client.clicid == 1


def test_apply_success(mock_db_connection):
    table = MagicMock()
    table.focus.return_value = "item1"
    table.item.return_value = (1, "Developer", "FullTime")
    mock_db_connection.fetchall.return_value = []

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        client.apply(table)
        mock_showinfo.assert_called_with(
            "Thanks", "Your application has been submitted"
        )


def test_apply_already_applied(mock_db_connection):
    table = MagicMock()
    table.focus.return_value = "item1"
    table.item.return_value = (1, "Developer", "FullTime")
    mock_db_connection.fetchall.return_value = [(1,)]

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        client.apply(table)
        mock_showinfo.assert_called_with(
            "Oops", "It seems like you have already applied to this job"
        )


def test_delet(mock_db_connection):
    table = MagicMock()
    table.focus.return_value = "item1"
    table.item.return_value = (1, "Developer", "FullTime")

    with (
        patch("tkinter.messagebox.showinfo") as mock_showinfo,
        patch("app.modules.client.myapp") as mock_myapp,
    ):
        client.delet(table)
        mock_showinfo.assert_called_with(
            "Thanks", "Your application has been Deleted"
        )
        mock_myapp.assert_called_once()


def test_showalljobs(mock_db_connection):
    table = MagicMock()
    mock_db_connection.fetchall.return_value = [
        (1, "Dev", "FullTime", "Corp A", "City A", "BSc", "1", 5000),
        (2, "QA", "PartTime", "Corp B", "City B", "MSc", "3", 6000),
    ]

    client.showalljobs(table)

    assert table.insert.call_count == 2
    table.insert.assert_any_call(
        "",
        0,
        text="",
        values=(1, "Dev", "FullTime", "Corp A", "City A", "BSc", "1", 5000),
    )


def test_show_myapplications(mock_db_connection):
    table = MagicMock()
    mock_db_connection.fetchall.return_value = [
        (10, "Analyst", "FullTime", "Data Inc.", "Remote", "Stats", "2", 7000),
    ]
    client.clicid = 1

    client.show_myapplications(table)

    assert table.insert.call_count == 1
    table.insert.assert_called_with(
        "",
        0,
        text="",
        values=(
            10,
            "Analyst",
            "FullTime",
            "Data Inc.",
            "Remote",
            "Stats",
            "2",
            7000,
        ),
    )


def test_sort_alljobs(mock_db_connection):
    table = MagicMock()
    with patch("app.modules.client.search_d", create=True) as mock_search_d:
        mock_search_d.get.return_value = "JobRole"

        client.sort_alljobs(table)
        table.delete.assert_called_once_with(*table.get_children())
        mock_db_connection.execute.assert_called_with(
            "select job.JID,job.JobRole,job.JobType, recruiter.CompanyName"
            ", recruiter.CompanyLocation, job.Qualification, job.MinExp,"
            " job.Salary from hireme.job JOIN hireme.recruiter ON "
            "job.rid=recruiter.rid order by JobRole"
        )
