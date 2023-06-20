import boto3
import json
import os
import logging

 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

 

def lambda_handler(event, context):
    sc = boto3.client('servicecatalog')
    cc = boto3.client('codecommit')

 

    portfolio_name = 'My Portfolio'
    repository_name = 'MyRepo'

 

    try:
        commit_id = event['Records'][0]['codecommit']['references'][0]['commit']
        commit = cc.get_commit(repositoryName=repository_name, commitId=commit_id)
        files = commit['commit']['tree']['tree']
    except Exception as e:
        logger.error("Error getting commit details: %s", e)
        raise

 

    for file in files:
        if not file['absolutePath'].endswith('.json'):
            continue

 

        product_name = os.path.splitext(file['absolutePath'])[0]

 

        try:
            blob = cc.get_blob(repositoryName=repository_name, blobId=file['blobId'])
            template = json.loads(blob['content'])
        except Exception as e:
            logger.error("Error getting file content: %s", e)
            continue

 

        try:
            portfolio_id = ''
            portfolios = sc.list_portfolios()
            for portfolio in portfolios['PortfolioDetails']:
                if portfolio['DisplayName'] == portfolio_name:
                    portfolio_id = portfolio['Id']
                    break
            if not portfolio_id:
                response = sc.create_portfolio(
                    AcceptLanguage='en',
                    DisplayName=portfolio_name,
                    ProviderName='My Company',
                    Description='This is my first portfolio'
                )
                portfolio_id = response['PortfolioDetail']['Id']

 

            product_id = ''
            products = sc.search_products_as_admin()
            for product in products['ProductViewDetails']:
                if product['ProductViewSummary']['Name'] == product_name:
                    product_id = product['ProductViewSummary']['ProductId']
                    break
            if not product_id:
                response = sc.create_product(
                    AcceptLanguage='en',
                    Name=product_name,
                    Owner='My Company',
                    Description='This is my first product',
                    Distributor='My Company',
                    SupportDescription='Support Description',
                    SupportEmail='test@example.com',
                    SupportUrl='http://www.example.com',
                    ProductType='CLOUD_FORMATION_TEMPLATE',
                    Tags=[],
                    ProvisioningArtifactParameters={
                        'Name': 'v1',
                        'Description': 'Version 1',
                        'Info': {
                            'LoadTemplateFromURL': json.dumps(template)
                        }
                    }
                )
                product_id = response['ProductViewDetail']['ProductViewSummary']['ProductId']

 

            response = sc.associate_product_with_portfolio(
                AcceptLanguage='en',
                ProductId=product_id,
                PortfolioId=portfolio_id
            )
        except Exception as e:
            logger.error("Error creating or updating portfolio/product: %s", e)
            continue

 

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda execution completed!')
    }