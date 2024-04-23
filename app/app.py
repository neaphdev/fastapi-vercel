import google.generativeai as genai
from fastapi import FastAPI
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = FastAPI()

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")


@app.get("/generate/")
async def generate_text(prompt: str):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=200, num_return_sequences=1)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_text": text}


@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_app():
    return app
