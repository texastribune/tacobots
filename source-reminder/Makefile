deploy: install-deps
	zip -r deployment_package *
	aws lambda update-function-code \
	--region us-east-1 \
		--function-name sourceReminder \
		--zip-file fileb://deployment_package.zip
	rm deployment_package.zip

install-deps:
	pip3 install -t $$(pwd) -r $$(pwd)/requirements.txt

# builds to .aws-sam directory cleaner than "install-deps"
# todo: switch deploy from manually zipping the directory to using AWS SAM
sam-build:
	sam build --use-container

# docker commands
build-image:
	docker build -t source-reminder/lambda:0.1 .

run-container: build-image
	docker run \
		--rm -it -d \
		-p 9000:8080 \
		source-reminder/lambda:0.1

test-container: run-container
	curl -XPOST \
		"http://localhost:9000/2015-03-31/functions/function/invocations" \
		-d '{}'