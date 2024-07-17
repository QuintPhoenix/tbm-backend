from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import llms
import images
import docs.scripts as doc
from fastapi.responses import FileResponse
from os import environ

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class LLMRequest(BaseModel):
    title: str
    section: str

class wordDocRequest(BaseModel):
    title : str
    imageLinks : list
    body : list


@app.post("/gemini")
async def gemini(body: LLMRequest):
    return llms.gemini_gen(body.title, body.section)

@app.post("/gemini-alt")
async def gemini_alt(body: LLMRequest):
    return llms.gemini_alt_gen(body.title, body.section)

@app.post("/mistral")
async def mistral(body: LLMRequest):
    return llms.mistral_gen(body.title, body.section)

@app.post("/falcon")
async def falcon(body: LLMRequest):
    return llms.falcon_gen(body.title, body.section)

@app.post("/llama")
async def falcon(body: LLMRequest):
    return llms.llama_gen(body.title, body.section)

@app.get("/images/pexels")
async def pexels(location: str | None = "Goa"):
    return images.get_pexels(location)

@app.get("/images/pixabay")
async def pixabay(location: str | None = "Goa"):
    return images.get_pixabay(location)

@app.post("/generate")
async def generate(body : wordDocRequest):
    doc_name = doc.generate_doc(body.title,body.imageLinks,body.body)
    generated_doc_path = environ.get("GENERATED_DOC_PATH")
    return FileResponse(path=(generated_doc_path + doc_name))
