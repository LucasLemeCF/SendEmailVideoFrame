provider "aws" {
  region = var.aws_region
}

# Função Lambda para envio de e-mail
resource "aws_lambda_function" "register_user" {
  function_name = "frame_sendemail_function" # Nome fixo da função Lambda

  handler = "sendemail.lambda_handler" # Atualizado para o handler da função de procesamento
  runtime = "python3.11"
  role    = aws_iam_role.lambda_sendemail_role.arn
  timeout = 60 # Definir o tempo de execução para 1 minuto

  # Caminho para o código da função Lambda.
  filename         = "../lambda/sendemail/sendemail_lambda_function.zip"
  source_code_hash = filebase64sha256("../lambda/sendemail/sendemail_lambda_function.zip")
}

# Role para Lambda
resource "aws_iam_role" "lambda_sendemail_role" {
  name = "lambda_execution_role" # Nome fixo da role

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}
