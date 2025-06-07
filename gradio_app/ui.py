import gradio as gd  
import requests

class GradioUi(): 
    def __init__(self): 
        self.url = "http://backend_service:8709/askQuestion/" 
        self.chatbot = gd.Chatbot(
            elem_id="mychatbot",
            label="MyCustom Chatbot",
            placeholder="Hello! How can I assist you today?",
            show_copy_button=True,
            layout="bubble",
            render_markdown=True,
            allow_file_downloads= False,
            sanitize_html = True,
            height = "#mychatbot{height: 80vh}"
        )
        
    def respond(self, message, history):
        payload = {
            "query": message,
            "isChat": True
        }
        res = requests.post(self.url, json=payload)
        try:
            return res.json()["answer"]
        except Exception as e:
            return f"Error: {str(e)}"
 
        
    def launchBot(self): 
        chat = gd.ChatInterface(
            fn=self.respond,
            chatbot=self.chatbot,
            title="Echo Bot",
            examples = ["Hello", "How are you?", "Tell me a joke", "What is Gradio?"],
            theme="default",
            save_history = False, 
            fill_height=True,
            stop_btn = True,
            autoscroll	=True,
            css="#mychatbot{height: 80vh}"
        )

        chat.launch(share=True, server_name="0.0.0.0", server_port=8710)

if __name__ == "__main__":
    GradioUi().launchBot()




