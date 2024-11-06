import replicate

output = replicate.run(
    "google-deepmind/gemma2-9b-it:24464993111a1b52b2ebcb2a88c76090a705950644dca3a3955ee40d80909f2d",
    input={
        "top_k": 50,
        "top_p": 0.9,
        "prompt": "Write me a poem about Machine Learning.",
        "temperature": 0,
        "max_new_tokens": 512,
        "repetition_penalty": 1.2
    }
)

# The google-deepmind/gemma2-9b-it model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/google-deepmind/gemma2-9b-it/api#output-schema
    print(item, end="")
