import pytest
from typer.testing import CliRunner
from frontend.cli import app
from backend.exceptions import ChronicleBaseException

runner = CliRunner()

def test_cli_list_empty():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    # It should print out "No knowledge has been archived yet" or the table.
    # Since the mock DB might be empty, it should be fine.

def test_cli_view_not_found():
    result = runner.invoke(app, ["view", "9999"])
    assert result.exit_code == 1
    assert "No archive found" in result.stdout

def test_cli_delete_aborted():
    result = runner.invoke(app, ["delete", "9999"], input="n\n")
    # Aborted by user
    assert result.exit_code == 1

def test_cli_delete_not_found():
    result = runner.invoke(app, ["delete", "9999"], input="y\n")
    assert result.exit_code == 1
    assert "No archive found" in result.stdout
