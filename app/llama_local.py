from llama_cpp import Llama

# LLaMA modelini başlat
llama_model = Llama(
    model_path="../models/llama/capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4,  # Sistemine göre 6 veya 8 yapabilirsin
    verbose=False
)

def ask_llama(prompt: str) -> str:
    response = llama_model(prompt, max_tokens=512, stop=["</s>"])
    return response["choices"][0]["text"].strip()
