import gradio as gd  
import requests

class GradioUi(): 
    def __init__(self): 
        self.url = "http://backend_service:8709/askQuestion/" 
        self.chatbot = gd.Chatbot(
            elem_id="mychatbot",
            label="Email Creator",
            placeholder="Hello! How can I assist you today?",
            show_copy_button=True,
            layout="bubble",
            render_markdown=True,
            allow_file_downloads= False,
            sanitize_html = True,
            height = "#mychatbot{height: 65vh}"
        )
        
    def respond(self, message, history, tone, length):
        payload = {
            "query": message,
            "tone": str(tone), 
            "length": str(length)
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
            theme="default",
            examples=[
                ["Write an email requesting a meeting with my manager"],
                ["Draft a professional email to follow up on a job application"],
                ["Create an email to inform the team about a deadline extension"],
                ["Write an email apologizing for missing a meeting"],
                ["Compose an email to congratulate a colleague on their promotion"],
                ["Write an email requesting feedback on my recent presentation"]
            ],
            type="messages",
            save_history = False, 
            fill_height=True,
            stop_btn = True,
            autoscroll	=True,
            additional_inputs=[
                gd.Slider(minimum=0, maximum=100, step=1, value=50, label="Email Tone "), 
                gd.Slider(minimum=0, maximum=1000, step=1, value=50, label="Email Length")
            ],
            css="#mychatbot{height: 65vh}"
        )

        chat.launch(share=True, server_name="0.0.0.0", server_port=8710)

if __name__ == "__main__":
    GradioUi().launchBot()




