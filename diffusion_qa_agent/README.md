
### Diffusion Q&A Agent

To start working with the agent

1. Install necessary dependencies

```bash
pip install -r requirements.txt
```

2. Create `.env` file where put `OPENAI_API_KEY` and `TELEGRAM_TOKEN`
   
Example `.env` file:
   
```
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_TOKEN=your_telegram_bot_token
```

3. Run the application

```bash
python app.py
```

### Features

- Answers questions using OpenAI's GPT models.
- Integrates with Telegram for real-time Q&A.
- Supports conversation history for context-aware answers.

### Usage

- Start a chat with your Telegram bot.
- Ask any question; the bot will reply using AI-generated answers.

### Project Structure

```
.
├── app.py
├── requirements.txt
├── README.md
└── .env
```

### Notes

- Ensure your OpenAI API key has sufficient quota.
- The bot only responds to messages in private chats or where it is mentioned.

### License

MIT License