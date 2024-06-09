import asyncio
import threading
import pygame


from pyjy.utils import logger

from llm.Bedrock import BedrockClaude3

from llm.LLMInterface import LLMInterface

from pyjy.message import Message
from pyjy.constants import SceneType



class Xiaoer:
    
    
    
    
    def __init__(self):
        self.id_in_game = 1
        self.cn_name = "店小二"
        self.en_name = "Xiaoer"
        self.sub_scene_id = 1
        
        self.x = 18
        self.y = 20
        
        self.sub_scene_location = (18, 20)
        
        self.message_history = []
        
        self.message_number_to_send = 100
        
        self.conversation_target_id = ""
        self.conversation_target_cn_name = ""
        self.waiting_for_LLM_response = False
        
        self.controller = None
        
        self.head_img = None
        
    def register_to_controller(self, controller):
        self.controller = controller
        
    def get_talker_img(self):
        if self.head_img is None:
            img = self.controller.texture_manager.get_texture_pygame(SceneType.SUB_SCENE, 2559)[0]
            img_size = img.get_size()
            img_scaled = pygame.transform.scale(img, (img_size[0]*1.5, img_size[1]*1.5))
            self.head_img = img_scaled
        return self.head_img
        
    def update(self, time_delta):
        pass
    
    def at_msg_receive(self, message:Message):
        
        if message is None:
            return
        
        if message.receiver_id != self.id_in_game:
            return
        
        self_chinese_name = self.cn_name
        
        logger.log_info(str(message))
        
        
        
        self.message_history.append(message)
        
        text = str(message.text)
        
        sender_chinese_name = message.sender_cn_name
        
        # convert self.message_history to a string
        # only keep the last 100 messages
        
        selected_message_history = self.message_history[-self.message_number_to_send:]
        
        # calling each message's game_formated_str method to convert them to a new list:
        converted_message_history = [message.game_formated_str() for message in selected_message_history]
        
        message_history_str = "\n".join(converted_message_history)
        
        
        prompt_message = f'''
这是一个关于金庸的武侠小说的开放式游戏，我是河洛客栈的店小二，我所在的地方就是河洛客栈，
一个游戏玩家({sender_chinese_name})给我发了这个消息：{text}，请帮我生成一个符合中国古代武侠游戏的回复。
作为游戏早期的NPC，而且是一个和游戏主线无关的NPC，我不会对游戏的主线剧情做出任何的回答。
你给我的回复不要有任何的解释，直接发给我需要回复的内容。
因为我作为一个NPC程序，我只能转发你的回复，你多余的解释会让我的回复显得不像是一个NPC的回复。
注意也不要在回复中加上 店小二说，店小二回答等字样，因为我所在的PRG程序会生成这部分，你不需要生成。

为了更好地生成回复，我会把之前的对话记录也一并发给你，以下是我之前和这位玩家对话记录。
{message_history_str}
        '''
        
        logger.log_info(f"Prompt message to LLM: {prompt_message}")
        
        self.conversation_target_id = message.sender_id
        self.conversation_target_cn_name = sender_chinese_name
        self.waiting_for_LLM_response = True
        # Pass handle_llm_response as callback function
        LLMInterface.process_llm_response(prompt_message, self.handle_llm_response)
            
            

    

    def handle_llm_response(self, response):
        response_str = str(response)
        response_str = response_str.replace("'", "\\'")
        logger.log_info(f"Response string: {response_str}")
        
        llm_response_message = Message(self.id_in_game, self.cn_name, self.conversation_target_id, self.conversation_target_cn_name, response_str)  
        
        self.message_history.append(llm_response_message)
        
        if self.controller is not None:
            self.controller.message_from_npc(llm_response_message)
        



