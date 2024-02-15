import torch
from transformers import MarianMTModel, MarianTokenizer

class Translator:
    def __init__(self, model_name="D:\\Users\\aa762344\Desktop\GOKAI\\2_models\\opus-mt-tc-big-tr-en", is_cuda = True):
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() and is_cuda == True else "cpu")
        self.model = None
        self.tokenizer = None
        self.load_model_and_tokenizer()

    def load_model_and_tokenizer(self):
        print(f"Device: {self.device}")
        # Load the model and tokenizer
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)
        self.model.to(self.device)
        self.model.eval()
  

    def tokenize_text(self, src_text):
        # Tokenize the source text
        src_text_tokenized = self.tokenizer(src_text, return_tensors="pt", padding=True, truncation=True)
        src_text_tokenized = {key: val.to(self.device) for key, val in src_text_tokenized.items()}
        return src_text_tokenized

    def generate_translation(self, src_text_tokenized):
        # Generate translations
        with torch.no_grad():
            translated = self.model.generate(**src_text_tokenized)
        return translated

    def decode_translations(self, translated):
        # Decode and return translations
        translations = [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        full_translation = " ".join(translations)
        return full_translation

    def get_timing_results(self, all_start_time, trans_start_time, generate_start_time, generate_end_time, decode_start_time, decode_end_time, trans_end_time, all_end_time):
        results = {
            "TokenizeTime": generate_start_time - trans_start_time,
            "GenerateTime": generate_end_time - generate_start_time,
            "DecodeTime": decode_end_time - decode_start_time,
            "TranslationTime": trans_end_time - trans_start_time,
            "TotalTime": all_end_time - all_start_time 
        }
        return results