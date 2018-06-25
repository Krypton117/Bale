import requests
import json
import re


from chalice import Chalice


app = Chalice(app_name='helloworld')

@app.route('/')
def index():
	return data

@app.route('/get_userstories')
def get_userstories():
	url = "https://api.trello.com/1/lists/5a8a8d847e06f130c40fb24f/cards?fields=name,id"
	querystring = {"key":"326ecc8e5aaeba3263fabd5da2947bcb","token":"0633646770e6ea79f7a75f5f20004713a75d9ae6c8ce7a114022d238efd20f1b"}
	response = requests.request("GET", url, params=querystring)
	data = response.json()
	return data


#TEST GET actions of card, with ID
'''
@app.route('/get_actions')
def get_usactions():
	global querystring
	url = "https://api.trllo.com/1/cards/id/actions"
	response = requests.request("GET", url, params=querystring)
	data = response.json()
	print data
'''

@app.route('/check_role')
def check_role():
	global rating
	
	userstories = get_userstories()
	data = []
	for v in userstories:
		#print v['name']
		print v['actions']
		searchrole = re.search(r'As a', v['name'])
		error = []
		rating = 0
		if searchrole:
			#print 'Role was found.'
			rating += 5
			'''data.append({'Userstory': v['name'], 'Rating': rating})'''
		else:
			error.append('Role was not found')
			print 'Role was not found.'
		searchfeature = re.search(r'I want to', v['name'])
		if searchfeature:
			rating += 10
		else:
			error.append('Feature was not found')
			print 'Feature was not found.'
		searchreason = re.search(r' so ', v['name'])
		if searchreason:
			rating += 5
		else: 
			error.append('Reason was not found')
			print 'Reason was not found'
			
		length_userstory = len(v['name'])
		if length_userstory < 150:
			rating += 2
		else:
			print 'Userstory too long'
			error.append('Userstory too long')
		if length_userstory > 20:
			rating += 16
		
		if not searchrole and not searchreason and not searchfeature:
			rating = 0	
		data.append({'Userstory': v['name'], 'Rating': rating, 'Errors': error})
		

	print(data)
	return data


check_role()


