import json
import os
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

from botocore.exceptions import ClientError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.sendemail.sendemail import (lambda_handler, process_message,
                                     send_email_error, send_email_success)


class TestLambdaFunction(TestCase):

    @patch('src.sendemail.sendemail.requests.post')
    def test_send_email_success(self, mock_post):
        mock_post.return_value.status_code = 202
        destinatario = "test@example.com"
        url_download = "http://example.com/download"
        send_email_success(destinatario, url_download)
        mock_post.assert_called_once()

    @patch('src.sendemail.sendemail.requests.post')
    def test_send_email_error(self, mock_post):
        mock_post.return_value.status_code = 500
        destinatario = "test@example.com"
        url_download = "http://example.com/download"
        send_email_success(destinatario, url_download)
        mock_post.assert_called_once()

    @patch('src.sendemail.sendemail.send_email_success')
    @patch('src.sendemail.sendemail.send_email_error')
    def test_process_message_success(self, mock_send_email_success, mock_send_email_error):
        message = {
            'body': {
                'status': 'sucesso',
                'to_address': 'test@example.com',
                'url_download': 'http://example.com/download'
            }
        }
        response = process_message(message)
        # mock_send_email_success.assert_called_once_with('test@example.com', 'http://example.com/download')
        # mock_send_email_error.assert_not_called()
        self.assertEqual(response['statusCode'], 200)

    @patch('src.sendemail.sendemail.send_email_success')
    @patch('src.sendemail.sendemail.send_email_error')
    def test_process_message_error(self, mock_send_email_success, mock_send_email_error):
        message = {
            'body': {
                'status': 'erro',
                'to_address': 'test@example.com'
            }
        }
        response = process_message(message)
        # mock_send_email_success.assert_not_called()
        # mock_send_email_error.assert_called_once_with('test@example.com')
        self.assertEqual(response['statusCode'], 200)

    @patch('src.sendemail.sendemail.process_message')
    @patch('src.sendemail.sendemail.send_email_error')
    def test_lambda_handler(self, mock_send_email_error, mock_process_message):
        mock_process_message.return_value = {'statusCode': 200}
        event = {
            'Records': [{
                'body': {
                    'status': 'sucesso',
                    'to_address': 'test@example.com',
                    'url_download': 'http://example.com/download'
                }
            }]
        }
        context = {}
        response = lambda_handler(event, context)
        # mock_process_message.assert_called_once()
        # mock_send_email_error.assert_not_called()
        self.assertEqual(response['statusCode'], 200)