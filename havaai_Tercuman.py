from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi import Request
import time
import havaai_Translator_cl 

app = FastAPI() 
templates = Jinja2Templates(directory="templates")

Translator_Cuda = havaai_Translator_cl .Translator(model_name="models\\tr_en\\opus-mt-tc-big-tr-en", is_cuda = True)
Translator_Cpu = havaai_Translator_cl .Translator(model_name="models\\en_tr\\opus-mt-tc-big-en-tr", is_cuda = False)

 
''' class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    translation: str
    timing_results: dict '''

@app.post("/tercuman", response_class=JSONResponse)
async def translate_text(request: Request, text: str = Form(...), language: str = Form(...)):

    if language == "tr-en":
        Translator_Selected = Translator_Cuda
    elif language=="en-tr":
        Translator_Selected = Translator_Cpu
    else:
        print("dil seçiminde hata")
    all_start_time = time.time()
    trans_start_time = time.time()
    src_text_tokenized = Translator_Selected.tokenize_text(text)
    generate_start_time = time.time()

    translated = Translator_Selected.generate_translation(src_text_tokenized)

    generate_end_time = time.time()
    decode_start_time = time.time()

    translation_result = Translator_Selected.decode_translations(translated)

    decode_end_time = time.time() 
    trans_end_time = time.time()
    all_end_time = time.time()

    translation_metric = Translator_Selected.get_timing_results(all_start_time, trans_start_time, generate_start_time, generate_end_time, decode_start_time, decode_end_time, trans_end_time, all_end_time)

    return JSONResponse({"translation_result": translation_result, "translation_metric": translation_metric})

