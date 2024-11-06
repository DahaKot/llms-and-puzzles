import torch
from transformers import pipeline

print("calling the API")
pipe = pipeline(
    "text-generation",
    model="google/gemma-2-9b",
    device="cuda",  # replace with "mps" to run on a Mac device
)

text = "Once upon a time,"
print(text)
outputs = pipe(text, max_new_tokens=256)
print("Outputs: ", outputs)
response = outputs[0]["generated_text"]
print(response)
