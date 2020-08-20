deploy:
	zip deployment_package lambda_function.py
	aws lambda update-function-code \
	--region us-east-1 \
		--function-name HoedownHelper \
		--zip-file fileb://deployment_package.zip
	rm deployment_package.zip