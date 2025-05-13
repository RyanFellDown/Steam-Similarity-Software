import json


def get_response_code(logs, target_url):
    responses = []
    main_response = None

    for log in logs:
        log_message = json.loads(log['message'])['message']
        if log_message["method"] == "Network.responseReceived":
            response = log_message["params"]["response"]
            responses.append(response)
            if response["url"] == target_url:
                main_response = response
    return(main_response['status'])