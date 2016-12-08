from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UnicodeText

Base = declarative_base()

class DbObject(object):
	def __init__(self):
		self.engine = create_engine('sqlite:///song_db.db')
		Base.metadata.create_all(self.engine)

	def start_session(self):
		Session = sessionmaker(bind = self.engine)
		self.session = Session()

		return self

	def clear_db_data(self):
		Base.metadata.drop_all(self.engine)
	
		Base.metadata.create_all(self.engine)

class SongDetails(Base):
	__tablename__ = 'songdetails'
	song_id = Column(Integer, primary_key=True)
	song_name = Column(String(40))
	song_lyrics = Column(UnicodeText(64))