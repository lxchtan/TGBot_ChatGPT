import logging
from os import environ as env
from dotenv import load_dotenv  # if you dont have dotenv yet: pip install python-dotenv
from copy import deepcopy

import telebot
import openai
import json
import tiktoken

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
  """Returns the number of tokens used by a list of messages."""
  try:
    encoding = tiktoken.encoding_for_model(model)
  except KeyError:
    encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
    num_tokens = 0
    for message in messages:
      num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
      for key, value in message.items():
        num_tokens += len(encoding.encode(value))
        if key == "name":  # if there's a name, the role is omitted
          num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens
  else:
    raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()
bot = telebot.TeleBot(env["BOT_API_KEY"])
openai.api_key = env["OPENAI_API_KEY"]
input_file = output_file = env["TGBOT_LOG"]

with open(input_file, 'r', encoding='utf-8') as f:
  dialogue_history = json.load(f)

history = deepcopy(dialogue_history)

@bot.message_handler(func=lambda message: True)
def get_chatgpt(message):
  global dialogue_history
  global history

  while num_tokens_from_messages(history) > 3584:
    history = history[:1] + history[3:]

  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages= history + [{"role": "user", "content": message.text}],
      max_tokens=512,
  )

  respond_text = response["choices"][0]["message"]["content"]

  bot.send_message(message.chat.id, respond_text, parse_mode="Markdown")
  
  new_his = [
    {"role": "user", "content": message.text},
    {"role": "assistant", "content": respond_text}
  ]

  history.extend(new_his)
  dialogue_history.extend(new_his)

  with open(output_file, 'w') as fw:
    json.dump(dialogue_history, fw, indent=2, ensure_ascii=False)

bot.infinity_polling()
