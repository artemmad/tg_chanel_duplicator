<div align="center">
<h1>Telegram channel duplicator</h1>
<img
  height="90"
  width="90"
  alt="tg logo"
  src="https://telegram.org/img/t_logo.svg?1"
  align="left"
/>
<h3>Python client-bot for copying content from telegram channels, chats and private messages to their channels. It works even if the telegram chanel have "Restrict Saving Content" flag on</h3>
</div>
<br/>
<br/>
<br/>

## Installation

* You need [Python](https://www.python.org/) >= 3.7
* `# pip install -r requirements.txt`
* Rename `config.json.example` to `config.json`
* `$ python main.py`

## Configuration

Before the first run, you need to configure the program using the `config.json` file.

* `account_phone` - Your phone number from your telegram account.<br/>

* `account_api_id` and `account_api_hash` - You need to get these values on the website https://my.telegram.org/ by creating your application. [Instructions](https://core.telegram.org/api/obtaining_api_id)<br/>
* `delay` - Delay per second between checks for new messages.
* `groups` - List of groups, there may be several.
  * `name` - Group name.
  * `inputs` - **The names of the dialogs** in your account where the messages will come from.
  * `outputs` - Names of dialogs where messages will be copied.
  * `words` - If the list is not empty, only messages that contain one of the words from this list will be copied.
  
<h3>You can also configure the bot from the telegram, for more information send a message `~!help` in favorites while the bot is running</h3>


Project is based on another [project](https://github.com/deFiss/telegram_channel_duplicator) that duplicates messages form tg.