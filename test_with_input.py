import pytest
import subprocess
import requests
from unittest.mock import patch, MagicMock, mock_open

@pytest.fixture
def mock_requests(monkeypatch):
    mock_post = MagicMock()
    monkeypatch.setattr(requests, 'post', mock_post)
    return mock_post

def test_main(mock_requests, monkeypatch, capsys):

    mock_requests.side_effect = [
        # Response for registration
        MagicMock(json=lambda: {'message': "New user 'user123' registered successfully."}),
        # Response for login
        MagicMock(json=lambda: {'message': "Login successful for user 'user123'."}),
        # Response for file upload
        MagicMock(json=lambda: {'message': "File uploaded successfully."}),
        # Response for logout
        MagicMock(json=lambda: {'message': "User 'user123' logged out successfully."})
    ]

    monkeypatch.setattr('builtins.input', lambda _: '1')  # Simulate user choosing '1' for registration
    monkeypatch.setattr('getpass.getpass', lambda _: 'pass123')  # Simulate user inputting password
    with patch('builtins.open', mock_open(read_data='user123\npass123\npass123\n5\n')):
        subprocess.run(['python', 'test.py'], check=True)

    captured = capsys.readouterr()
    assert "New user 'user123' registered successfully." in captured.out
    assert "Login successful for user 'user123'." in captured.out
    assert "File uploaded successfully." in captured.out
    assert "User 'user123' logged out successfully." in captured.out
