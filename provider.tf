provider "aws" {
  region = "eu-west-2"
}

terraform {
  required_providers {
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.2"
    }
    aws = {
      source = "hashicorp/aws"
    }
  }
  backend "s3" {
    bucket         = "tf-state-serv-cata"
    key            = "serv-cata-tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "serv-cata-tfstate-lock"
  }
}
