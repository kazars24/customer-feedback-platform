from llama_cpp import Llama


SYSTEM_TOKEN = 1788
USER_TOKEN = 1404
BOT_TOKEN = 9225
LINEBREAK_TOKEN = 13
ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}


def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model, system_prompt):
    system_message = {
        "role": "system",
        "content": system_prompt
    }
    return get_message_tokens(model, **system_message)


def get_saiga_model(model_path, n_ctx=2000):
    return Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_parts=1,
    )


class Agent():
    def __init__(self, model_path, system_prompt, token=ROLE_TOKENS["bot"], n_ctx=2000, top_k=30, top_p=0.9, temperature=0.5, repeat_penalty=1.1):
        self.model = get_saiga_model(model_path, n_ctx)
        self.system_prompt = system_prompt
        self.token = token
        self.top_k = top_k
        self.top_p = top_p
        self.temperature = temperature
        self.repeat_penalty = repeat_penalty

    def interact(self, input):
        system_tokens = get_system_tokens(self.model, self.system_prompt)
        tokens = system_tokens
        self.model.eval(tokens)

        message_tokens = get_message_tokens(model=self.model, role="user", content=input)
        role_tokens = [self.model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
        tokens += message_tokens + role_tokens
        generator = self.model.generate(
            tokens,
            top_k=self.top_k,
            top_p=self.top_p,
            temp=self.temperature,
            repeat_penalty=self.repeat_penalty
        )

        output = []
        for token in generator:
            token_str = self.model.detokenize([token]).decode("utf-8", errors="ignore")
            tokens.append(token)
            if token == self.model.token_eos():
                break
            output.append(token_str)
        return ''.join(output)
