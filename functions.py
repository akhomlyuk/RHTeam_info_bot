import requests
import json
from bs4 import BeautifulSoup
from name_that_hash import runner
from icecream import ic
import logging

result_api_url = 'https://ctftime.org/api/v1/results/'
event_info_api_url = 'https://ctftime.org/api/v1/events/'
rht_url = 'https://ctftime.org/api/v1/teams/186788/'
# rht_results = "https://ctftime.org/team/186788"
# top_teams_ru_url = 'https://ctftime.org/stats/RU'

header = {'Host': 'ctftime.org',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.199 Safari/537.36',
          'Referer': 'https://ctftime.org/'}

RHT = 186788


def rating(results: list):
    team_points = results[0]
    best_points = results[1]
    team_place = results[2]
    weight = results[3]
    total_teams = results[4]
    place_k = 1 / team_place
    points_k = team_points / best_points
    result = (points_k + place_k) * weight / 1 / 1 + (team_place / total_teams)
    return result


def rht_best_res() -> list:
    try:
        with requests.Session() as s:
            response = s.get(result_api_url, headers=header)
            response_text = response.json()
            results = []
            results_for_menu = []
            for key, value in response_text.items():
                for i in value['scores']:
                    if i.get('team_id') == RHT:
                        results.append(
                            {value.get('title'): {'Place': int(i.get('place')), 'CTF points': float(i.get('points'))}})
                        sorted_data = sorted(results, key=lambda x: x[list(x.keys())[0]]['Place'])
            for i in sorted_data[:10]:
                for j in i:
                    place = i[j].get("Place")
                    if i[j].get("Place") == 1:
                        results_for_menu.append(f'🥇 {j} - <b>{place}</b>')
                    elif i[j].get("Place") == 2:
                        results_for_menu.append(f'🥈 {j} - <b>{place}</b>')
                    elif i[j].get("Place") == 3:
                        results_for_menu.append(f'🥉 {j} - <b>{place}</b>')
                    else:
                        results_for_menu.append(f'🪣 {j} - <b>{place}</b>')
            return [sorted_data, results_for_menu]
    except Exception as e:
        logging.error(e)
        pass


def rht_info() -> dict:
    with requests.Session() as s:
        try:
            rht = s.get(rht_url, headers=header)
            rht = json.loads(rht.text)
        except json.decoder.JSONDecodeError:
            print('ctftime not available')
    return rht


def results_from_ctftime() -> dict:
    with requests.Session() as s:
        try:
            b = s.get(result_api_url, headers=header)
            b = json.loads(b.text)
        except json.decoder.JSONDecodeError:
            print('ctftime not available')
    return b


def event_information(event_id: int) -> dict:
    with requests.Session() as s:
        try:
            event_info = s.get(event_info_api_url + str(event_id) + '/', headers=header)
            event_info = json.loads(event_info.text)
        except json.decoder.JSONDecodeError:
            print('ctftime not available')
    return event_info


# def top_teams_ru() -> list:
#     with requests.Session() as s:
#         header = {
#             'Host': 'ctftime.org',
#             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
#             'Connection': 'close'
#         }
#         response = s.get(top_teams_ru_url, headers=header)
#         soup = BeautifulSoup(response.content, "html.parser")
#         table = soup.find("table", {"class": "table table-striped"})
#         results = []
#
#         for row in table.find_all("tr")[1:]:
#             cols = row.find_all("td")
#             place = cols[2].text.strip()
#             team_name = cols[4].text.strip()
#             points = cols[5].text.replace('*', '').strip()
#             results.append(
#                 {team_name: {'Place': int(place), 'CTF points': float(points)}})
#         results_for_menu = []
#         for i in results[:14]:
#             for j in i:
#                 results_for_menu.append(f'<b>{i[j].get("Place")}</b> {j} Points: <b>{i[j].get("CTF points")}</b>')
#         return results_for_menu


def hash_analyze(hash_string: str):
    try:
        if runner.api_return_hashes_as_dict([hash_string], {"popular_only": True}) == {hash_string: []}:
            text = runner.api_return_hashes_as_dict([hash_string])
            return text[hash_string]
        else:
            text = runner.api_return_hashes_as_dict([hash_string], {"popular_only": True})

            return text[hash_string]
    except Exception as e:
        ic(e)
        ic()
