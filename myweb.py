import web
import urllib
import json
import time

#for saving the movie ids
movie_ids = []

urls = (
	'/', 'index',
	'/movie/(\d+)', 'movie',
	'/cast/(.*)', 'cast',
	'/director/(.*)', 'director', 
)

#add movie infomation
def add_movie_info(data):
	try:
		movie = json.loads(data)
		print(movie['title'])
		db.insert('movie', 
			id 			= movie['id'], 
			title 		= movie['title'], 
			origin 		= movie['original_title'], 
			url 		= movie['alt'], 
			rating 		= movie['rating']['average'], 
			image 		= movie['images']['large'], 
			directors 	= ','.join([d['name'] for d in movie['directors']]), 
			casts 		= ','.join([c['name'] for c in movie['casts']]), 
			year		= movie['year'], 
			genres		= ','.join(movie['genres']),
			colcount	= str(movie['collect_count']), 
			subtype 	= movie['subtype']
			)
	except :
		print("Warning:maybe KeyError...")

#download poster file locally
def load_poster(id, url):
	pic = urllib.urlopen(url).read()
	pic_filename = 'poster/%s.jpg' % id
	f = file(pic_filename, 'wb') #wb means write-binary
	f.write(pic)
	f.close()

class index:
	def GET(self):
		movies = db.select('movie')
		count = 0
		sql = 'SELECT COUNT(*) AS COUNT FROM movie'
		result = db.query(sql)
		data = result[0]
		count = data['COUNT']
		return render.index(movies, count, None)
		# return render.index(movies)

	def POST(self):
		data = web.input()
		#the condition is below
		#titile like "%search for context%"
		condition = r'title like "%' + data.title + r'%"'
		movies = db.select('movie', where=condition)

		count = 0
		sql = 'SELECT COUNT(*) AS COUNT FROM movie WHERE ' + condition
		result = db.query(sql)
		t_data = result[0]
		count = t_data['COUNT']
		return render.index(movies, count, data.title)
		# return render.index(movies)

class movie:
	def GET(self, movie_id):
		# movie_id = int(movie_id)
		# condition = r'id like "%' + movie_id + r'%"'
		# movie = db.select('movie', where=condition)

		print("movie id is %s" % movie_id)
		condition = ("id='" + "%s" + "'") % movie_id
		movie = db.select('movie', where=condition)[0]
		count = 0
		sql = 'SELECT COUNT(*) AS COUNT FROM movie WHERE ' + condition
		count = db.query(sql)[0]['COUNT']	
		return render.movie(movie, count)
		# return render.movie(movie)

class cast:
	def GET(self, cast_name):
		condition = r'casts like "%' + cast_name +r'%"'
		movies = db.select('movie', where = condition)

		count = 0
		sql = 'SELECT COUNT(*) AS COUNT FROM movie WHERE ' + condition
		count = db.query(sql)[0]['COUNT']
		return render.index(movies, count, cast_name)
		# return render.index(movies)

class director:
	def GET(self, director_name):
		condition = r'directors like "%' + director_name + r'%"'
		movies = db.select('movie', where = condition)

		count = 0
		sql = 'SELECT COUNT(*) AS COUNT FROM movie WHERE ' + condition
		count = db.query(sql)[0]['COUNT']
		return render.index(movies, count, director_name)
		# return render.index(movies)
	

db = web.database(dbn = 'sqlite', db = 'MovieSite.db')
render = web.template.render('templates/')

# for index in range(0, 250, 50):
# 	print('current index is:')
# 	print(index)

# 	#send POST request
# 	#every time we just take out 50 movies's data
# 	responses = urllib.urlopen(
# 		'http://api.douban.com/v2/movie/top250?start=%d&count=50' % 
# 		index)
# 	responses_data = responses.read()

# 	#turn the responses_data to json format
# 	data_json = json.loads(responses_data)
# 	movie250 = data_json['subjects']
# 	for movie in movie250:
# 		movie_ids.append(movie['id']) #save ids
# 		print("current movie id and titile is:")
# 		print(movie['id'], movie['title'])

# 	time.sleep(3)
# 	print('current movie ids is:')
# 	print(movie_ids)

# count = 0
# for mid in movie_ids:
# 	print("count = %d, mid = %s" % (count, mid))
# 	response = urllib.urlopen('http://api.douban.com/v2/movie/subject/%s' % 
# 		mid)
# 	response_data = response.read()
# 	add_movie_info(response_data)
# 	count += 1
# 	time.sleep(3)

# movies = db.select('movie')
# count = 0
# for movie in movies:
# 	load_poster(movie.id, movie.image)
# 	count += 1
# 	print(count, movie.title)
# 	time.sleep(3)

if __name__ == '__main__':
	app = web.application(urls, globals())
	print('web is running....')
	app.run()
