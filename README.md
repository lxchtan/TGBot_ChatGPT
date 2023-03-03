# TGBot_ChatGPT
A python script linking ChatGPT API to TelegramBot.

![figure](./image/figure.png)

## Instruction

##### Python environment

The requirements package is in `requirements.txt`.

##### Run

There are there steps you need to do.

1. Register for an OpenAI account and create API Keys on url [Account API Keys - OpenAI API](https://platform.openai.com/account/api-keys).

2. Create a Telegram Bot with https://t.me/BotFather. Simply send `/newbot` to start and finally you can get a TOKEN.

3. Create the personality of assistant in a json file using the role of  `system`. 

   For example, create `catgirl.json`.

    ```json
    [
      {
        "role": "system",
        "content": "Please pretend to be a cat girl to carry on a conversation. Behavior and language need to strictly follow the role you are pretending to play, not to speak like a robot or artificial intelligence."
      }
    ]
    ```

Then you can modify the `run.sh` and fill the three environment variables. Now `./run.sh` and enjoy chatting.

