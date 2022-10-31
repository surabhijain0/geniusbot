# GeniusBot

## Overview

There's plenty of Discord bots that allow you to search up song lyrics, but few of these provide any other song information. GeniusBot provides extensive information from Genius on not just songs, but even albums and artists.

## How to run GeniusBot

1. **Clone the repository**  
Run the following command in order to clone the repository:
```bash
$ git clone https://github.com/surabhijain0/geniusbot
```

2. **Create a Discord bot account**  
Follow the steps at the [Discord Developer Portal](https://discord.com/developers/docs/getting-started#creating-an-app) on creating a bot account. Make sure to choose the bot scope, as well as the read messages, send messages, and send messages in threads permissions.

3. **Set up environment variables**  
Create a .env file in the project's root directory. Create a variable called `TOKEN` and set it to the token provided by Discord when you created your bot account.

4. **Install the project dependencies**  
Install the Discord, Requests, BeautifulSoup, and Dotenv Python libraries. The precise command will depend upon your OS and account permissions.

5. **Run the project**  
Simply run `main.py` to get your bot started.