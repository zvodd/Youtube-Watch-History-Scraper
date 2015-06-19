from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, asc, desc, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class HistoryEntry(Base):
	__tablename__ = 'videoshistory'
	id = Column(Integer, primary_key=True)
	vid = Column(String, nullable=False) 
	author_id = Column(String, nullable=False)
	title = Column(String, nullable=False)
	description = Column(String)
	time = Column(Integer, nullable=False)

class AppDatabase(object):
	youtube_db_name = "/youtube_history.db"

	def __init__(self, refresh=False):
		engine = create_engine('sqlite://'+self.youtube_db_name)
		self.engine = engine
		Base.metadata.bind = engine
		DBSession = sessionmaker()
		DBSession.bind = engine
		self.try_create_database()
		self.DBSession = DBSession

	def try_create_database(self, refresh=False):
		if refresh:
			Base.metadata.drop_all()
		if not self.engine.table_names():
			Base.metadata.create_all()

	@contextmanager
	def _session_scope(self, commit = False):
		"""Provide a transactional scope around a series of operations."""
		session = self.DBSession()
		try:
			yield session
			if commit:
				session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()

	def push_video_entry(self, vid, author_id, title, description, time):
		with self._session_scope(commit = True) as session:
			he = HistoryEntry()
			he.vid = vid
			he.author_id = author_id
			he.title = title
			he.description = description
			he.time = time
			session.add(he)