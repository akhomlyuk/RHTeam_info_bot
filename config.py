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
