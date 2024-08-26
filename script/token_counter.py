import tiktoken

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    print(f"[INFO] Calculating token count for provided string using encoding: {encoding_name}")
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(f"[INFO] Token count: {num_tokens}")
    return num_tokens
