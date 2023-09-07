import torch
from llama_cpp import Llama
torch.cuda.empty_cache()
import json

SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический анализатор отзывов покупателей. Ты получаешь на вход текст отзыва и даешь краткую характеристику для: персонал, очереди, чистота."
SYSTEM_TOKEN = 1788
USER_TOKEN = 1404
BOT_TOKEN = 9225
LINEBREAK_TOKEN = 13
MODEL_PATH = '/content/ggml-model-q4_1.bin'

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


def get_system_tokens(model, SYSTEM_PROMPT):
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    return get_message_tokens(model, **system_message)

def get_summary(reviews, config):
  PROMPT = "User: "
  for ind, review in enumerate(reviews):
    r = "Отзыв " + str(ind + 1) + ": " + review
    PROMPT += r
  user_message = PROMPT
  message_tokens = get_message_tokens(model=config["model"], role="user", content=user_message)
  role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
  tokens = config["tokens"]
  tokens += message_tokens + role_tokens
  generator = model.generate(
      tokens,
      top_k=config["top_k"],
      top_p=config["top_p"],
      temp=config["temperature"],
      repeat_penalty=config["repeat_penalty"]
  )
  answer = ""
  for token in generator:
      token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
      tokens.append(token)
      if token == model.token_eos():
          break
      amswer += token_str
  return answer
def get_reviews(data, address):
  reviews = []
  for r in data[address]:
    reviews.append(r["text"])
  return reviews
def read_json(path):
  with open(path, "r") as fp:
    x5 = json.load(fp)
  x5_dict = {}
  for url in x5.keys():
    x5_dict[x5[url]["address"]] = x5[url]["reviews_list"]
  return x5_dict
