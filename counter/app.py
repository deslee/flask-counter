from flask import Flask, jsonify, request
from mongoengine import *
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adioasdjasiodjasiodasjd'
app.config['SITE_NAME'] = 'deslee'
app.config['MONGODB_SETTINGS'] = {
	'DB': 'deslee-counter',
}
db = MongoEngine(app)

class UniqueVisitor(db.Document):
	ip = StringField(max_length=100, required=True)
	site = StringField(max_length=100, required=True, unique_with='ip')
	count = IntField()

class Counter(db.Document):
	site = StringField(max_length=100, required=True, unique=True)
	count = IntField()
	
	def __str__(self):
		return "{}: {}".format(self.site,self.count)

def findOne(Model, **query):
	try:
		return Model.objects.get(**query)
	except:
		return None

@app.route('/counter')
def hello():
	counter = findOne(Counter, site=app.config['SITE_NAME'])
	d = {}
	if counter:
		counter.count += 1
		counter.save()
		d['total'] = counter.count

		user = findOne(UniqueVisitor, ip=request.remote_addr, site=app.config['SITE_NAME'])
		if user:
			user.count += 1
			user.save()
			d['user'] = user.count
		else:
			user = UniqueVisitor(ip=request.remote_addr, site=app.config['SITE_NAME'], count=1)
			user.save()
			d['user'] = user.count

		uniques = UniqueVisitor.objects(site=app.config['SITE_NAME'])
		d['unique'] = len(uniques)	
		
	return jsonify(**d)
