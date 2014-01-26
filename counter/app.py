from flask import Flask, jsonify, request
from mongoengine import *
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adioasdjasiodjasiodasjd'
app.config['MONGODB_SETTINGS'] = {
	'DB': 'deslee-counter',
}
db = MongoEngine(app)

class Site(db.Document):
	name = StringField(max_length=100, required=True, unique=True)
	
	def __str__(self):
		return "{}: {}".format(self.site,self.count)

class UniqueVisitor(db.Document):
	ip = StringField(max_length=100, required=True)
	site = ReferenceField(Site, required=True, unique_with='ip')
	count = IntField()

def findOne(Model, **query):
	try:
		return Model.objects.get(**query)
	except:
		return None

@app.route('/counter/')
def hello():
	data = request.args['url']
	site = findOne(Site, name=data)

	if not site:
		site = Site(name=data)
		site.save()

	d = {}

	user = findOne(UniqueVisitor, ip=request.remote_addr, site=site)
	if user:
		user.count += 1
	else:
		user = UniqueVisitor(ip=request.remote_addr, site=site, count=1)

	user.save()
	d['user'] = user.count

	uniques = UniqueVisitor.objects(site=site)
	d['unique'] = len(uniques)	
	d['url'] = data

	d['total'] = sum([unique.count for unique in uniques])

	return jsonify(**d)
