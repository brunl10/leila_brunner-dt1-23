@app.route("/chat")
def call_huggingface_chat_model():
    model_id = req.args.get("model_id")
    logging.debug(f"The model ID for the Huggingface model is {model_id}")
    huggingface_token = req.args.get("huggingface_token")
    logging.debug(f"Huggingface API Token: {huggingface_token}")
    questions = req.args.get("input")
    data = query(
        {
            "inputs": f'{questions.replace("_"," ")}',
            "options": {"wait_for_model": True},
            "parameters": {"return_full_text": False, "max_time": 30},
        },
        model_id,
        huggingface_token,
    )
    logging.debug(f"Model output: {data}")

    # Handle unexpected response formats from Hugging Face
    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        output = jsonify({"ack": data[0]["generated_text"]})
    else:
        output = jsonify({"error": "Failed to get generated text", "details": data})

    output.headers.add("Access-Control-Allow-Origin", "*")
    return output
