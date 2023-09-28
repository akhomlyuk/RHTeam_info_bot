from functions import rht_best_res, rht_info, top_teams_ru
from config import *

rht_info = rht_info()
rht_best = rht_best_res()
top_ru = top_teams_ru()

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
⚙️ Прокси: <b>{' : '.join(str(c) for c in socks_cmds)}</b>
📈 Rate: <b>!rate очки_очки 1 место_место_вес_колво тим</b>
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

dante_socks = f'''<b>SOCKS5</b>

<b>ip</b>: 79.133.183.84
<b>port</b>: 4114
<code>dsocks:Z9MYa8HbYrOY4hcdOI8x</code>

https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-basic/'''

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