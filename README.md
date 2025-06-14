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

* You need [Python](https://www.python.org/) >= 3.13.3
* `# pip install -r requirements.txt`
* Rename `conf/config.json.example` to `conf/config.json`
* `$ python main.py`

## Configuration

Before the first run, you need to configure the program using the `conf/config.json` file.

* `account_phone` - Your phone number from your telegram account.<br/>

* `account_api_id` and `account_api_hash` - You need to get these values on the website https://my.telegram.org/ by creating your application. [Instructions](https://core.telegram.org/api/obtaining_api_id)<br/>
* `delay` - Delay per second between checks for new messages.
* `groups` - List of groups, there may be several.
  * `name` - Group name.
  * `inputs` - **The names of the dialogs** in your account where the messages will come from.
  * `outputs` - Names of dialogs where messages will be copied.
  * `words` - If the list is not empty, only messages that contain one of the words from this list will be copied.
  
<h3>You can also configure the bot from the telegram, for more information send a message `~!help` in favorites while the bot is running</h3>


## Using Docker

Download docker-compose.yaml and place it in folder where you would like.
Docker compose attaching the mount with temp database and config.js file.

Crete sub folder near downloaded docker-compose.yaml and name it `conf`.
Then fulfill `config.json` file like it described above and place it inside `conf` folder.

``cd`` to dirrectory with placed docker-compose file and run:

```bash
docker run --rm -it -v ${PWD}/conf:/app/conf --entrypoint /bin/sh madartem/telegramresender:latest
```

Then run inside sh inside container such comand:
```bash
python3 main.py
```

You will be promted to authentication dialog where you should place your code sended to you via telegram to provide authentication for telegram client. Your promt inside container would look like this:
```bash
# python3 main.py
2024-02-10T10:29:02.440556+0000 | INFO - Created by https://github.com/artemmad
2024-02-10T10:29:02.491128+0000 | INFO - Account authorization
Enter the code from the Telegram message: 81172
Signed in successfully as <YOUR TELEGRAM NAME WOULD BE HERE>
2024-02-10T10:29:11.346715+0000 | INFO - Account authorization was successful
2024-02-10T10:29:11.347315+0000 | DEBUG - cycle
```

Then exit container sh using exit command:
```bash
exit
```
In the next time you can start without attaching console, because in volume mounted you have stored authentication.

Now you can simply start by docker-compose:
```
docker-compose up
```

If all is ok and in container logs you have such lines you successfully installed solution:
```bash
docker-compose up
Creating network "telegram_channel_duplicator_default" with the default driver
Creating telegram_channel_duplicator_tg_re_sender_1 ... done
Attaching to telegram_channel_duplicator_tg_re_sender_1
tg_re_sender_1  | 2024-02-10T10:39:58.738940+0000 | INFO - Created by https://github.com/artemmad
tg_re_sender_1  | 2024-02-10T10:39:58.741724+0000 | INFO - Account authorization
tg_re_sender_1  | 2024-02-10T10:39:59.060881+0000 | INFO - Account authorization was successful
tg_re_sender_1  | 2024-02-10T10:39:59.061433+0000 | DEBUG - cycle

``` 

In next time you can use:

```
docker-compose up -d
```


# Dump one message by telegram message reference

Downloading supports only refs with such synthax ``https://t.me/c/<chat_id>/<message_id>``, example ``https://t.me/c/12345/11``.

You can run the solution locally or using docker to dump one message with all media attached to it. Downloading will work only 
if you bootstrap the solution succesfully and in ``conf/session`` folder exist valid and not expired session.

```bash

python3 download.py
2024-11-27T17:17:38.447285+0400 | INFO - Authorization successful
Enter the message link: 
https://t.me/c/xxxx/xxxx
2024-11-27T17:17:41.774873+0400 | INFO - Processing message URL: https://t.me/c/xxxx/xxx
2024-11-27T17:17:42.060434+0400 | INFO - Message text saved to downloads/message_xxx/message.txt
2024-11-27T17:20:01.460199+0400 | INFO - Media saved to downloads/message_xxx/be770dad-41a3-4a04-b8a1-0101f2f3df08.mp4

Process finished with exit code 0
```

Or you can simply provide link to telegram message by passing it to donwloader.py:

```bash
python3 download.py https://t.me/c/12345/11
```

The downloads could be found in ``/download/message_<message_id>`` folder

Project is based on another [project](https://github.com/deFiss/telegram_channel_duplicator) that duplicates messages form tg.