# makelaars-watchdog
Scraping and notification terminal application for multiple estate websites.
Based on [pararius-apartments-alert](https://github.com/LLagu/pararius-apartments-alert)

## Dependencies
Tested in python 3.8.17 on a Debian 12.
Only works on Linux based systems.
Python libraries: 'bs4', 'selenium', 'webdriver-manager','gtts', 'telegram_send', 'pysimplegui'


## Disclaimer
This is not meant to be user friendly nor to be the most efficient way to scrape websites.
I needed to parametrize pararius-apartments-alert so that I could quickly add and test other estate
websites on short notice. This translates in a "it just works" approach and requires to modify the code to suit your requirements.

## Telegram setup
This is a one-time setup.
1. Go to https://telegram.me/BotFather and send the message "/newbot" to the chat
2. Open the terminal and type "telegram-send --configure"
3. Copy and paste the token you received from BotFather in the terminal
4. Now you will receive a notification every time the parser detects a new accomodation


## How to use

You can use the existing websites as a guideline but in general you in `main.py` you need to:
1. Call `GetPageSource()` with your website url and the class name of the closest element that contains the href.
For example if your website has the properties listed as:

```
<h1>List of Links</h1>

<ul>
    <li class="list-item"><a href="https://example.com/apartment1">Link 1</a></li>
    <li class="list-item"><a href="https://example.com/apartment2">Link 2</a></li>
    <li class="list-item"><a href="https://example.com/apartment3">Link 3</a></li>
</ul>
```

you want to call 
`GetPageSource("https://example.com/searchURL", "list-item")`

or if `a` has a class:
```
<ul>
    <li class="list-item"><a class = "abc" href="https://example.com/apartment1">Link 1</a></li>
    <li class="list-item"><a class = "abc" href="https://example.com/apartment2">Link 2</a></li>
    <li class="list-item"><a class = "abc" href="https://example.com/apartment3">Link 3</a></li>
</ul>
```
then `GetPageSource("https://example.com/searchURL", "abc")`

2. Call `ParsePage()` with the following parameters:
    | Parameter   | Description  | Example      |
    |-------------|--------------|--------------|
    | `p_userUrl`               | Your website site url      | "https://example.com/searchURL"     |
    | `p_baseUrl`               | For logging purposes       | "example.com"      |
    | `p_messageToTheBroker`    | Specified in `message.txt` | "Hallo, ik zou deze te dure kast graag snel willen zien."     |
    | `p_old_page_source`       | `GetPageSource()` output   | user_website_old_source where user_website_old_source = GetPageSource(...)     |
    | `p_className`             | See previous step          | "list-item"       |
    | `p_tag`                   | Tag of where teh href is   | "a"     |
   

4. Run with `python3 main.py`

5. Profit (???)
  
