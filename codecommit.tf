resource "aws_codecommit_repository" "repo" {
  repository_name = "MyRepo" # update this with your repository name
  description     = "This is my repository"
}
