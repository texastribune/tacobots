
def lambda_handler(data, context):
    # print logs to aws for debugging / development
    print(f"Received event:\n{data}\nWith context:\n{context}")

    event = data['event']
    thread = event['ts']
    channel = event['channel']


    challenge_answer = data.get("challenge")
    if challenge_answer:
        return {
            'statusCode': 200,
            'body': challenge_answer
        }
    else:
        return {
            "channel": channel,
            "thread_ts": thread,
            "text": "Responding in a thread, whoo!"
        }