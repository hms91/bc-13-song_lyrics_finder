# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import html5lib
from model_base import DbObject, SongDetails
from prettytable import PrettyTable

database = DbObject()
session = database.start_session().session


class FindLyrics(object):

    def __init__(self):
        self.base_url = 'http://api.genius.com'
        self.headers = {
            'Authorization': 'Bearer P5vQ2aTZs_6Vn2RL1fE-FUDKSMOzMw50CvtRpDBwngPUiUkXB3folUYRt5UMyNBO'}
        self.search_url = self.base_url + "/search?"

    def find(self, query_string):
        # Returns a list of songs that match the criteria.
        # search_for = query_string.replace(' ', '%20')
        search_for = '%20'.join(query_string)
        search_query = self.search_url + 'q=' + search_for
        try:
            response = requests.get(
                search_query, headers=self.headers)
        except requests.exceptions.ConnectionError:
            return "Error: Please check your Connection :("

        json = response.json()
        results = json['response']['hits']

        return results

    def view_by_id(self, song_id):
        # View song lyrics based on it's id. Should be optimized by checking if
        # there's a local copy before checking online.

        song_details = {}
        try:
            song_id = int(song_id)
        except:
            return "Invalid Input!"

        this_song = session.query(SongDetails).get(song_id)

        if this_song is not None:
            song_details['song_id'] = this_song.song_id
            song_details['song_name'] = this_song.song_name
            song_details['song_lyrics'] = this_song.song_lyrics.encode('utf-8')

        else:
            # search_for = int(song_id)
            # data = {'q': search_for}
            # try:
            #     response = requests.get(
            #         self.search_url, data=data, headers=self.headers)
            # except:
            #     raise requests.exceptions.ConnectionError(
            #         'Error: Please check your Connection')
            by_id = self.base_url + "/songs/"
            search_query = by_id + str(song_id)
            try:
                response = requests.get(search_query, headers=self.headers)
            except requests.exceptions.ConnectionError:
                return "Error: Please check your Connection :("

            json = response.json()

            results = json["response"]["song"]["url"]

            # result_list = []
            # count = 0
            # for i in range(len(results)):
            #     if count > 1:
            #         break
            #     else:
            #         song_id = results[i]['result']['id']
            #         title = results[i]['result']['title']
            #         artist = results[i]['result']['primary_artist']['name']
            #         url = results[i]['result']['url']
            #         count += 1
            #     result_list.append([song_id])
            #     result_list.append([title])
            #     result_list.append([artist])
            #     result_list.append([url])

            lyrics_page_url = results

            res = requests.get(lyrics_page_url)

            soup = BeautifulSoup(res.text, "html5lib")

            lyrics = soup.find("lyrics", class_="lyrics").text.encode('utf-8')

            song_details['song_name'] = json['response']['song']['title']
            song_details['song_id'] = json['response']['song']['id']
            song_details['song_lyrics'] = lyrics

        return song_details

    def save_song(self, song_id):
        # Store song details and lyrics locally.
        song_details = self.view_by_id(song_id)
        this_song = SongDetails(song_id=song_details['song_id'], song_name=song_details[
                                'song_name'], song_lyrics=song_details['song_lyrics'].decode('utf-8'))
        session.add(this_song)
        session.commit()

    def clear(self):
        # Clear entire local song database.
        database.clear_db_data()


song = FindLyrics()

# this_one = "Power Trip"
# # id =  91686
# print song.find(this_one)
# print song.view_by_id(id)
# song.save_song(id)

# print session.query(SongDetails.song_id, SongDetails.song_name, SongDetails.song_lyrics).first()
# song.clear()

# print song.view_by_id(id)
# this_song = "black beatles in the city"
# ress = song.find(this_song)

# t = PrettyTable(['ID','Title','Artist'])
# for i in range(len(ress)):
# 	song_id = ress[i]['result']['id']
# 	title = ress[i]['result']['title']
# 	artist = ress[i]['result']['primary_artist']['name']

# 	t.add_row([song_id, title, artist])
# print t

# the_ = song.view_by_id('7731')
# song.save_song(378195)
# lyrics = session.query(SongDetails).get(378195).song_lyrics
# print type(lyrics)
# # lyrics = str(lyrics)
# lyrics = lyrics.encode('utf-8')
# # print (isinstance(lyrics, str))
# print lyrics
# print int('ego')

# lyrics = session.query(SongDetails).get(378195)
# print lyrics.song_lyrics
# song.clear()