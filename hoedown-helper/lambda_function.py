def lambda_handler(event, context):
    # print logs to aws for debugging / development
    print(f"Received event:\n{event}\nWith context:\n{context}")

    challenge_answer = event.get("challenge")
    
    return {
        'statusCode': 200,
        'body': challenge_answer
    }