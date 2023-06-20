resource "aws_lambda_function" "lambda" {
  function_name    = "service-catalog-lambda"
  handler          = "lambdafunction.lambda_handler"
  runtime          = "python3.9"
  timeout          = 60
  memory_size      = 128
  role             = aws_iam_role.lambda_role.arn
  source_code_hash = filebase64sha256("./resources/lambda_function.py")
  filename         = "resources/lambda_function.zip"
}