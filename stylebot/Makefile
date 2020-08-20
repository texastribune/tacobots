deploy:
	npm install
	zip -r deployment_package .
	aws lambda update-function-code \
	--region us-east-1 \
		--function-name QueryStyleGuide \
		--zip-file fileb://deployment_package.zip
	rm deployment_package.zip