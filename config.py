import os
from icecream import ic

bot_token = os.getenv('rht_info_bot_token')
results_cmds = ['!results', '!stats', '!best']
info_cmds = ['!info', '!information', '!инфо']
flag_cmds = ['!flags', '!flagbot']
commands_cmds = ['cmds', 'commands']
git_cmds = ['rht-git', 'rht_git', '!git']
buttons_cmds = ['!ссылки', '!links']
brief_cmds = ['!brief', 'brief', 'бриф', '!бриф']
menu_cmds = ['!menu', '!меню', '!start']
ngrok_cmds = ['!ngrok']
del_cmds = ['!del']
wiki_cmds = ['!wiki']
send_sticker_cmds = ['!го', '!go', '!вперед']
top_cmds = ['!top', '!ru', '!топ']
send_photo_cmds = ['!last']
todo_cmds = ['!todo']
user_id_cmds = ['!id']
next_event_cmds = ['!next']

commands = f'''📜 Information: <b>{' : '.join(str(c) for c in info_cmds)}</b>
📈 Results: <b>{' : '.join(str(c) for c in results_cmds)}</b>
🔖 Menu: <b>{' : '.join(str(c) for c in menu_cmds)}</b>
📝 Список дел: <b>{' : '.join(str(c) for c in todo_cmds)}</b>
🏁 Flag bot: <b>{' : '.join(str(c) for c in flag_cmds)}</b>
⚙️ RHT git: <b>{' : '.join(str(c) for c in git_cmds)}</b>
📌 URLs: <b>{' : '.join(str(c) for c in buttons_cmds)}</b>
👨‍🚀 Brief: <b>{' : '.join(str(c) for c in brief_cmds)}</b>
🔝 Top RU: <b>{' : '.join(str(c) for c in top_cmds)}</b>
📚 Wiki: <b>{' : '.join(str(c) for c in wiki_cmds)}</b> пример: !wiki linux
⛓ Ngrok: <b>{' : '.join(str(c) for c in ngrok_cmds)}</b>
⌨️ Commands: <b>{' : '.join(str(c) for c in commands_cmds)}</b>'''

links = f'''🔖 Ссылки:
⚙️ <a href="https://github.com/RedHazzarTeam-CODEBY-GAMES/">Github</a>
🃏 <a href="https://ctftime.org/team/186788">Ctftime</a>
🏁 <a href="tg://resolve?domain=rhtflagsbot">Flagbot</a>
☎️ <a href="https://discord.gg/V6Ba8qf2">Discord</a>
'''
