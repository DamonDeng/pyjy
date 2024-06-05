import boto3
import json


class BedrockClaude3:
    # model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    # model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

    @staticmethod
    def invoke(prompt, model_id = "anthropic.claude-3-sonnet-20240229-v1:0"):
        try:
            response = BedrockClaude3.client.invoke_model(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 1024,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": prompt}],
                            }
                        ],
                    }
                ),
            )

            # Process and print the response
            result = json.loads(response.get("body").read())
            input_tokens = result["usage"]["input_tokens"]
            output_tokens = result["usage"]["output_tokens"]
            output_list = result.get("content", [])

            print("Invocation details:")
            print(f"- The input length is {input_tokens} tokens.")
            print(f"- The output length is {output_tokens} tokens.")

            print(f"- The model returned {len(output_list)} response(s):")
            
            response_text = ""
            
            for output in output_list:
                print(output["text"])
                response_text += output["text"]

            return response_text
        except Exception:
            print("Couldn't invoke Claude3 model")
            raise

class BedrockMistral:
    

    client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

    @staticmethod
    def invoke(prompt, model_id = "mistral.mistral-large-2402-v1:0"):
    

        try:
            # Mistral instruct models provide optimal results when
            # embedding the prompt into the following template:
            instruction = f"<s>[INST] {prompt} [/INST]"

            # model_id = "mistral.mixtral-8x7b-instruct-v0:1"
            # model_id = "mistral.mistral-large-2402-v1:0"

            body = {
                "prompt": instruction,
                "max_tokens": 200,
                "temperature": 0.5,
            }

            response = BedrockMistral.client.invoke_model(
                modelId=model_id, body=json.dumps(body)
            )

            response_body = json.loads(response["body"].read())
            outputs = response_body.get("outputs")

            completions = [output["text"] for output in outputs]
            
            # convert the completions into a single string
            completions_str = "\n".join(completions)

            return completions_str

        except Exception:
            print("Couldn't invoke Mixtral 8x7B")
            raise
        
        
class BedrockLlama3:
    # model_id = "anthropic.mistral-20230531:0"

    client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

    @staticmethod
    def invoke(prompt, model_id = "meta.llama3-70b-instruct-v1:0"):
    

        try:
            
            # Set the model ID, e.g., Llama 3 8B 70B Instruct.
            # model_id = "meta.llama3-8b-instruct-v1:0"
            # model_id = "meta.llama3-70b-instruct-v1:0"

            # Embed the message in Llama 3's prompt format.
            prompt_content = f"""
            <|begin_of_text|>
            <|start_header_id|>user<|end_header_id|>
            {prompt}
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>
            """

            # Format the request payload using the model's native structure.
            request = {
                "prompt": prompt_content,
                # Optional inference parameters:
                "max_gen_len": 512,
                "temperature": 0.5,
                "top_p": 0.9,
            }

            # Encode and send the request.
            response = BedrockLlama3.client.invoke_model(body=json.dumps(request), modelId=model_id)

            # Decode the native response body.
            model_response = json.loads(response["body"].read())

            # Extract and print the generated text.
            response_text = model_response["generation"]
            print(response_text)

            return response_text

        except Exception:
            print("Couldn't invoke Llama 3 70B")
            raise



