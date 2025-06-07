from vllm import LLM, SamplingParams
import torch
from huggingface_hub import login
import nest_asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import socket
from dotenv import load_dotenv
import os



class ModelCall():
    def __init__(self, llm, temperature: float = 0.65, top_p: float = 0.95, max_tokens: int = 512):
        self.llm = llm
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    def makeQuery(self, query):
        self.sampling_params = SamplingParams(
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens
        )
        if not any(word in query.lower() for word in ["email", "mail", "send an email", "write an email", "compose email"]):
            self.messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a strict assistant that only helps with writing emails. "
                        "If a user gives a prompt that is not related to writing an email, "
                        "you will ask them to provide a clear instruction to write an email."
                    )
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        else:
            self.messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful email writing assistant. "
                        "You are going to write an email based on the user's prompt. "
                        "You will write the email in a professional tone."
                    )
                },
                {
                    "role": "user",
                    "content": query
                }
            ]

    def retQuery(self):
        outputs = self.llm.chat(self.messages, self.sampling_params)
        return outputs[0].outputs[0].text


def create_app(modelName):
    app = FastAPI()
    nest_asyncio.apply()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    llmQNA = ModelCall(modelName)

    class QueryRequest(BaseModel):
        query: str
        isChat: bool

    @app.get("/")
    def home():
        return {"answer": "FastAPI is running!"}

    @app.post("/askQuestion")
    @app.post("/askQuestion/")
    def askQuestion(data: QueryRequest):
        query = data.query
        llmQNA.makeQuery(query)
        answer = llmQNA.retQuery()
        return {"answer": answer}

    return app


def main():
    load_dotenv()
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    login(token=os.getenv("keys"))

    model_name = "unsloth/Qwen2.5-0.5B-Instruct"
    llm = LLM(model=model_name, dtype="float16")


    app = create_app(llm)

    ip_address = socket.gethostbyname(socket.gethostname())
    print(f"Your local IP address: {ip_address}")

    uvicorn.run(app, host="0.0.0.0", port=8709)


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support() 
    main()
