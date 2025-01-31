from unittest.mock import patch, MagicMock
from main import main


def test_main_success():
    with patch(
        "main.check_environment", return_value="config"
    ) as mock_check_environment, patch("main.TranscriberApp") as mock_TranscriberApp:
        mock_app_instance = MagicMock()
        mock_TranscriberApp.return_value = mock_app_instance

        main()

        mock_check_environment.assert_called_once()
        mock_TranscriberApp.assert_called_once_with("config")
        mock_app_instance.run.assert_called_once()
