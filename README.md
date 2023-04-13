![Wynncord](.github/assets/Wynncord_banner.png)
<center>
A modern bot for Wynncraft utility commands built with <a href="https://discordpy.readthedocs.io/en/stable/">discord.py</a>
</center>

![Discord](https://img.shields.io/discord/1093752105703047198?label=Server&logo=Discord)

## About
I have created this program without profit motive to help the Wynncraft community (and for fun). Currently, I do not possess much experience in developing Discord bots (or programming in general). Therefore, any contribution is welcome!

[Invite link](https://discord.com/api/oauth2/authorize?client_id=1090759373783056475&permissions=139586717760&scope=bot)

## Install
REQS: Python V3.11.3 | MongoDB

First install all the dependencies with:
```
pip install requests discord.py python-dateutil python-dotenv
```

Create a '.env' file inside the directory:
```
TOKEN=(your bot token)
MONGO_URI=(your mongodb uri)
```

Run main.py
```
python3 main.py
```
## Contribution
For now the bot is in an alpha state, i am still creating features and improving existing ones for performance/user experience. Any PR is welcome!, also you can check out how the development is going on our [Discord server](https://discord.gg/x349Me85Rm)

## TODO
* Add mongoDB implementation for data stored in jsons (warnotifs).
* Add player professions command
* Add guild stats command.