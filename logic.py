import requests
from bs4 import BeautifulSoup
import html5lib
from model_base import DbObject, SongDetails

database = DbObject()
session = database.start_session().session

class FindLyrics(object):
	def __init__(self):
		self.base_url = 'http://api.genius.com'
		self.headers = {'Authorization': 'Bearer FFu14c1hWkoJWFtfoi7UNJk9o_vRPvflLHk8yt3IZa9Kj-4AmUR9UlEFpID9ITpH'}
		self.search_url = self.base_url + "/search"

	def find(self, query_string):
	# Returns a list of songs that match the criteria. 
		search_for = query_string.replace(' ','%20')
		data = {'q': search_for}
		try:
			response = requests.get(self.search_url, data=data, headers=self.headers)
		except:
			raise requests.exceptions.ConnectionError('Error: Please check your Connection')

		json = response.json()
		results = json['response']['hits']
		
		return results

	def view_by_id(self, song_id):
	# View song lyrics based on it's id. Should be optimized by checking if there's a local copy before checking online. 
		song_details = {}

		this_song = session.query(SongDetails).get(song_id)

		if this_song is not None:
			song_details['song_id'] = this_song.song_id
			song_details['song_name'] = this_song.song_name
			song_details['song_lyrics'] = this_song.song_lyrics.encode('utf-8')
		
		else:
			search_for = int(song_id)
			data = {'q': search_for}
			try:
				response = requests.get(self.search_url, data=data, headers=self.headers)
			except:
				raise requests.exceptions.ConnectionError('Error: Please check your Connection')

			json = response.json()

			results = json["response"]["hits"]

			result_list = []
			count = 0
			for i in range(len(results)):
				if count > 1:
					break
				else:
				    song_id = results[i]['result']['id']
				    title = results[i]['result']['title']
				    artist = results[i]['result']['primary_artist']['name']
				    url =  results[i]['result']['url']
				    count += 1
			        result_list.append([song_id])
			        result_list.append([title])
			        result_list.append([artist])
			        result_list.append([url])

			lyrics_page_url = result_list[3]

			url_ = ''.join(lyrics_page_url)

			res = requests.get(url_)

			soup = BeautifulSoup(res.text, "html5lib")

			lyrics = soup.find("lyrics", class_="lyrics").text.encode('utf-8')

			song_id_ = result_list[0]
			song_id_ = map(str, song_id_) 
			song_id_ = ''.join(song_id_)
			song_id_ = int(song_id_)

			song_name_ = result_list[1]
			song_name_ = ''.join(song_name_)

			song_details['song_id'] = song_id_
			song_details['song_name'] = song_name_
			song_details['song_lyrics'] = lyrics


		return song_details

	def save_song(self, song_id):
	# Store song details and lyrics locally.
		song_details = self.view_by_id(song_id)
		this_song = SongDetails(song_id=song_details['song_id'],song_name=song_details['song_name'],song_lyrics=song_details['song_lyrics'].encode('utf-8'))
		session.add(this_song)
        session.commit()		

	def clear(self):
	# Clear entire local song database. 
		database.clear_db_data()

song = FindLyrics()
this_one = "PowerTrip"
# id =  91686
print song.find(this_one)
# print song.view_by_id(id)
# song.save_song(id)

# print session.query(SongDetails.song_id, SongDetails.song_name, SongDetails.song_lyrics).first()
# song.clear()

# print song.view_by_id(id)
