import os
from functions import rht_best_res, rht_info, top_teams_ru
from icecream import ic

rht_info = rht_info()
rht_best = rht_best_res()
top_ru = top_teams_ru()

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

top10_results = f'''Best 9 results: {round(rht_best[1], 3)} + CODEBY org(45.82) = <b>{rht_info["rating"]["2023"]["rating_points"]}</b>\n
{rht_best[2][0]}
{rht_best[2][1]}
{rht_best[2][2]}
{rht_best[2][3]}
{rht_best[2][4]}
{rht_best[2][5]}
{rht_best[2][6]}
{rht_best[2][7]}
{rht_best[2][8]}'''

rht_summary = f'''🌍 Worldwide position: <b>{rht_info["rating"]["2023"]["rating_place"]}</b>
🇷🇺 RU position: <b>{rht_info["rating"]["2023"]["country_place"]}</b>
🎯 Rating points: <b>{rht_info["rating"]["2023"]["rating_points"]}</b>
🚩 Team ID: <b>{rht_info["id"]}</b>
https://ctftime.org/team/186788'''

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

ngrok = [f'''$ cat ~/.config/ngrok/ngrok.yml

<code>version: "2"
authtoken: NGROK_TOKEN
tunnels:
  first:
    addr: 4444
    proto: tcp
  second:
    addr: 3333
    proto: tcp</code>

<b>$ ngrok start --all</b>''']


