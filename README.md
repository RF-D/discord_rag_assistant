# Discord Bot with LangChain Integration

This repository contains a Discord bot that utilizes LangChain for question answering and context retrieval. The bot is designed to help users with programming-related questions and provide relevant answers based on the channel's context.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Support](#support)

## Prerequisites

Before running the bot, make sure you have the following prerequisites:

1. Python 3.9 or higher
2. A Discord account and a server to add the bot to
3. OpenAI API key (optional, for using the GPT-4o model)
4. Pinecone API key and index name (optional, for using the Pinecone vector database)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/your-username/discord_rag_assistant.git
cd discord_rag_assistant
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory of the project and add the following environment variables:

```
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

Replace `your_discord_bot_token`, `your_openai_api_key`, and , `your_pinecone_api_key` with your actual values.

2. Create a new Discord bot application and obtain its token. Follow the Discord documentation to create a bot and obtain its token: https://discordpy.readthedocs.io/en/latest/discord.html#creating-a-bot-account

3. Replace `your_discord_bot_token` in the `.env` file with the token you obtained from the Discord developer portal.

## Usage

1. Run the bot:

```bash
python my_bot.py
```

2. Invite the bot to your Discord server by following the Discord documentation: https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-invite-my-bot-to-servers

3. Use the `!ask` command in the Discord channel to ask questions. The bot will retrieve relevant context from the channel's history and use LangChain to generate an answer.

## Support

If you encounter any issues or have questions, feel free to open an issue in this repository or reach out to me directly.