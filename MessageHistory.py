
from langchain.memory import ChatMessageHistory

questions = [   
                "How big do you want your house to be?", 
                "What are 3 most important things for you in choosing this property?", 
                "Which amenities would you like?", 
                "Which transportation options are important to you?",
                "How urban do you want your neighborhood to be?",       
            ]
answers = [
    "A comfortable three-bedroom house with a spacious kitchen and a cozy living room.",
    "A quiet neighborhood, good local schools, and convenient shopping options.",
    "A backyard for gardening, a two-car garage, and a modern, energy-efficient heating system.",
    "Easy access to a reliable bus line, proximity to a major highway, and bike-friendly roads.",
    "A balance between suburban tranquility and access to urban amenities like restaurants and theaters."
]




class CustomChatMessageHistory:
    def __init__(self):
        self.messages = ChatMessageHistory()
        self.messages.add_user_message("")

        
        for question, answer in zip(questions, answers):
            self.messages.add_ai_message(question)
            self.messages.add_user_message(answer)
        


    def add_ai_message(self, message: str):
        self.messages.add_ai_message(message)

    def get_questions(self):
        return " ".join(questions)

    def add_user_message(self, message: str):
        self.messages.add_user_message(message)

    def get_messages(self):
        return self.messages.messages

    def __str__(self):
        return f"ChatMessageHistory(messages={self.messages.messages})"