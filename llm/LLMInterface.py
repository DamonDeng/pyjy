import threading

from llm.Bedrock import BedrockClaude3
from llm.Bedrock import BedrockMistral
from llm.Bedrock import BedrockLlama3

class LLMInterface:
    
    Claude3_Sonet = "claude-3-sonet"
    Claude3_Opus = "claude-3-opus"
    Claude3_Haiku = "claude-3-haiku"
    Mistral_7B = "mistral-7b"
    Mistral_8x7B = "mistral-8x7b"
    Llama3_8B = "llama-7b"
    Llama3_70B = "llama-70b"
    Mistral_Large = "mistral-large"
    
    name_to_id = {
        Claude3_Sonet: "anthropic.claude-3-sonnet-20240229-v1:0",
        Claude3_Opus: "anthropic.claude-3-opus-20240229-v1:0",
        Claude3_Haiku: "anthropic.claude-3-haiku-20240307-v1:0",
        Mistral_7B: "mistral.mistral-7b-instruct-v0:2",
        Mistral_8x7B: "mistral.mixtral-8x7b-instruct-v0:1",
        Llama3_8B: "meta.llama3-8b-instruct-v1:0",
        Llama3_70B: "meta.llama3-70b-instruct-v1:0",
        Mistral_Large: "mistral.mistral-large-2402-v1:0",
    }

    

    @staticmethod
    def invoke(model_name, prompt):
        if model_name in [LLMInterface.Claude3_Sonet, LLMInterface.Claude3_Opus, LLMInterface.Claude3_Haiku]:
            return BedrockClaude3.invoke(prompt, LLMInterface.name_to_id[model_name])
        elif model_name in [LLMInterface.Mistral_7B, LLMInterface.Mistral_8x7B, LLMInterface.Mistral_Large]:
            return BedrockMistral.invoke(prompt,LLMInterface.name_to_id[model_name])
        elif model_name in [LLMInterface.Llama3_8B, LLMInterface.Llama3_70B]:
            return BedrockLlama3.invoke(prompt,LLMInterface.name_to_id[model_name])
        else:
            raise ValueError(f"Invalid model name: {model_name}")
        
    @staticmethod
    def process_llm_response(prompt_message, callback):
        # Create a new thread to invoke the LLM service
        t = threading.Thread(target=LLMInterface.invoke_llm_service, args=(prompt_message, callback))
        t.start()

    @staticmethod
    def invoke_llm_service(prompt_message, callback):
        # Invoke the LLM service
        
        # response = LLMInterface.invoke('claude-3', prompt_message)
        # response = LLMInterface.invoke(LLMInterface.Llama_70B, prompt_message)
        response = LLMInterface.invoke(LLMInterface.Claude3_Sonet, prompt_message)
        
        
        # logger.log_info(f"Response from LLM: {str(response)}")
        
        # Call the callback function with the response
        callback(response)