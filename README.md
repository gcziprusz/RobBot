RobBot
======

RobBot is a Python Chat Bot that replies to your tweets.


INTRO:
======
This is a small python utility that uses a python 
twitter api wrapper (https://code.google.com/p/python-twitter/) and personalityforge's 
Chatbot API (http://www.personalityforge.com/chatbotapi.php) and responds to your twitter messages.


INSTALL:
========
You need a API keys from both twitter and personalityforge 
(https://dev.twitter.com) (http://www.personalityforge.com/newuser.php)

Once you have these API keys you should create a file called ".rob_bot_keystore" 
and save it to your HOME directory.

Copy and paste your API keys in the order shown below to .rob_bot_keystore file:

{replace with TWITTER OAUTH TOKEN}<br/>
{replace with TWITTER OAUTH TOKEN SECRET}<br/>
{replace with TWITTER CONSUMER KEY}<br/>
{replace with TWITTER CONSUMER SECRET}<br/>
{replace with personalityforge's SECRET KEY}<br/>
{replace with personalityforge's API KEY}<br/>
{replace with TWITTER NAME for example @gcziprusz}<br/>
{replace with your chatbots ID (read up how you can create your own at http://www.personalityforge.com)}<br/>
{replace with an integer  >= 10 to define how often twitter should be checked}

You are ready to run RobBot:
"python RobBot.py"
