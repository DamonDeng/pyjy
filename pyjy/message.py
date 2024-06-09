

class Message:
    
    def __init__(self, sender_id, sender_cn_name, receiver_id, receiver_cn_name, text):
        self.sender_id = sender_id
        self.sender_cn_name = sender_cn_name
        self.receiver_id = receiver_id
        self.receiver_cn_name = receiver_cn_name
        
        self.text = text
        
    def game_formated_str(self):
        return f"{self.sender_cn_name}:\n {self.text}"
        
    def system_formated_str(self):
        return f"Message from {self.sender_cn_name} to {self.receiver_cn_name}: {self.text}"