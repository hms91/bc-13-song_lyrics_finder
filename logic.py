import requests
from bs4 import BeautifulSoup
import html5lib

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

		pass	
	def save_song(self, song_id):
	# Store song details and lyrics locally.

		pass
	def clear(self):
	# Clear entire local song database. 
		pass

song = FindLyrics()
this_one = "Capsized"
print song.find(this_one)