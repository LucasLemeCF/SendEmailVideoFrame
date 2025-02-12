import sys

sys.path.append('/opt/bin/')

import json

import requests

email_sender = "videoframeprofiap@gmail.com"
email_api_key = "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"
url_smtp = "https://api.brevo.com/v3/smtp/email"

def lambda_handler(event, context):
    for message in event['Records']:
        response = process_message(message)

        if not response['statusCode'] in [200, 201, 202]:
            to_address = message['body']['to_address']
            send_email_error(to_address)
    
    return response

def process_message(message):
    body_message = message['body']

    status = body_message['status']
    destinatario = body_message['to_address']

    print("Status: ", status)
    print("Destinatário:", destinatario)

    if status == "sucesso":
        url_download = body_message['url_download']
        print("URL Download:", url_download)
        response = send_email_success(destinatario, url_download)
    else:
        response = send_email_error(destinatario)

    return response

def send_email_success(destinatario, url_download):
    headers = {
        "api-key": email_api_key,
        "Content-Type": "application/json"
    }

    data = {
        "sender": {"email": email_sender},
        "to": [{"email": destinatario}],
        "subject": "Video Frame Pro",
        "htmlContent": "<html><body><h1>Link para download do .zip: {}</h1></body></html>".format(url_download)
    }

    try:
        response = requests.post(url_smtp, headers=headers, json=data)

        if response.status_code in [202, 201]:
            return {
                'statusCode': response.status_code,
                'body': json.dumps('E-mail enviado com sucesso!')
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps(f'Erro ao enviar o e-mail: {response.status_code}')
            }

    except Exception as e:
        return {
            'statusCode': "500",
            'body': json.dumps(f"Erro na requisição: {str(e)}")
        }

def send_email_error(destinatario):
    headers = {
        "api-key": email_api_key,
        "Content-Type": "application/json"
    }

    data = {
        "sender": {"email": email_sender},
        "to": [{"email": destinatario}],
        "subject": "Video Frame Pro",
        "htmlContent": "<html><body><h1>Erro ao processar o video</h1></body></html>"
    }

    try:
        response = requests.post(url_smtp, headers=headers, json=data)

        if response.status_code in [200, 201, 202]:
            return {
                'statusCode': response.status_code,
                'body': json.dumps('E-mail de erro enviado.')
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps(f"Erro ao enviar o e-mail de erro: {response.status_code}")
            }

    except Exception as e:
        return {
            'statusCode': "500",
            'body': json.dumps(f"Erro na requisição: {str(e)}")
        }