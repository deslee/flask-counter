from flask import Flask, jsonify, request
from mongoengine import *
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adioasdjasiodjasiodasjd'
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

@app.route('/counter/')
def hello():
	data = request.args['url']
	counter = findOne(Counter, site=data)

	if not counter:
		counter = Counter(site=data, count=0)

	d = {}
	counter.count += 1
	counter.save()
	d['total'] = counter.count

	user = findOne(UniqueVisitor, ip=request.remote_addr, site=data)
	if user:
		user.count += 1
		user.save()
		d['user'] = user.count
	else:
		user = UniqueVisitor(ip=request.remote_addr, site=data, count=1)
		user.save()
		d['user'] = user.count

	uniques = UniqueVisitor.objects(site=data)
	d['unique'] = len(uniques)	
	d['url'] = data

	return jsonify(**d)
