deploy: install-deps
	zip -r deployment_package *
	aws lambda update-function-code \
	--region us-east-1 \
		--function-name sourceReminder \
		--zip-file fileb://deployment_package.zip
	rm deployment_package.zip

install-deps:
	pip3 install -r $$(pwd) requirements.txt