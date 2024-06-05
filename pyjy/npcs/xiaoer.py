import asyncio
import threading


from pyjy.utils import logger

from llm.Bedrock import BedrockClaude3

from llm.LLMInterface import LLMInterface




class Xiaoer:
    
    message_received = ''
    message_history = []
    
    def __init__(self, message_respoder):
        self.message_responder = message_respoder
        
    def at_object_creation(self):
        # Set initial attributes
        self.db.health = 100
        self.db.strength = 10
        
        # self.llm_client = BedrockClaude3()
        self.message_history = []
        
        

    def process_llm_response(self, prompt_message, callback):
        # Create a new thread to invoke the LLM service
        t = threading.Thread(target=self.invoke_llm_service, args=(prompt_message, callback))
        t.start()

    def invoke_llm_service(self, prompt_message, callback):
        # Invoke the LLM service
        
        # response = LLMInterface.invoke('claude-3', prompt_message)
        # response = LLMInterface.invoke(LLMInterface.Llama_70B, prompt_message)
        response = LLMInterface.invoke(LLMInterface.Claude3_Sonet, prompt_message)
        
        
        logger.log_info(f"Response from LLM: {str(response)}")
        
        # Call the callback function with the response
        callback(response)

    def handle_llm_response(self, response):
        response_str = str(response)
        response_str = response_str.replace("'", "\\'")
        logger.log_info(f"Response string: {response_str}")
        
        full_response_str = f"店小二说道: {response_str}"
        # self.location.msg_contents(full_response_str, exclude=[self])
        
        self.message_history.append(full_response_str)
        
        self.message_responder.message_from_npc(response_str)

    def at_msg_receive(self, text):
        
        sender_chinese_name = "小虾米"
        self_chinese_name = "店小二"
        
        mentioned_me = False
        
        logger.log_info(f"Message received: {text}")
        
        self.message_history.append(text)
        
        text_str = str(text)
        # # if "小二" in text or "店小二" in text or "xiaoer" in text or "xiao er" in text:
        # # set the mentioned_me flag to True if the player mentioned the NPC
        # if "小二" in text_str or "店小二" in text_str or "xiaoer" in text_str or "xiao er" in text_str:
        #     mentioned_me = True
        
        # if (type and type == "whisper") or mentioned_me:
        #     quick_response_str = f"{self_chinese_name}说道: 哎! 客官稍候!"
        #     self.location.msg_contents(quick_response_str, exclude=[self])
        #     self.message_history.append(quick_response_str)
        
        prompt_message = f'''
这是一个关于金庸的武侠小说的开放式游戏，我是河洛客栈的店小二，我所在的地方就是河洛客栈，
一个游戏玩家({sender_chinese_name})给我发了这个消息：{text}，请帮我生成一个符合中国古代武侠游戏的回复。
作为游戏早期的NPC，而且是一个和游戏主线无关的NPC，我不会对游戏的主线剧情做出任何的回答。
你给我的回复不要有任何的解释，直接发给我需要回复的内容。
因为我作为一个NPC程序，我只能转发你的回复，你多余的解释会让我的回复显得不像是一个NPC的回复。
注意也不要在回复中加上 店小二说，店小二回答等字样，因为我所在的PRG程序会生成这部分，你不需要生成。
        '''
        
        # convert self.message_history to a string
        # only keep the last 100 messages
        message_history_str = "\n".join(self.message_history[-100:])
        
        prompt_message += f'''
为了更好地生成回复，我会把之前的对话记录也一并发给你，以下是我之前在这个房间听到对话记录。
以下是我在这个房间听到对话记录:
{message_history_str}
        '''
        
        logger.log_info(f"Prompt message to LLM: {prompt_message}")
        
        # Pass handle_llm_response as callback function
        self.process_llm_response(prompt_message, self.handle_llm_response)
            
            

