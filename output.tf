output "repository_name" {
  value = aws_codecommit_repository.repo.repository_name
}

output "pipeline_name" {
  value = aws_codepipeline.pipeline.name
}

output "lambda_function_name" {
  value = aws_lambda_function.lambda.function_name
}
