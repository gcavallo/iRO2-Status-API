#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# iRO2-Status-API
# http://github.com/gcavallo/iro2-status-api/

# Copyright (c) 2014 by Gabriel Cavallo <gabrielcavallo@mail.com>
# BSD 3-Clause License http://opensource.org/licenses/BSD-3-Clause


from gevent import monkey; monkey.patch_all()
import redis, bottle, arrow
import time, json, socket
import settings


servers = settings.SERVERS
r = redis.Redis(settings.CACHE['Hostname'], settings.CACHE['Port'])
bottle.TEMPLATE_PATH.insert(0, 'templates')
bottle.debug(settings.BOTTLE['Debug'])


@bottle.route('/')
def index():
	''' Return index html template on GET requests. '''
	return bottle.template('index', ttl=settings.CACHE['TTL'])


@bottle.route('/', method='POST')
def view_status():
	''' Return the status json string on POST requests. '''

	def get_status(address, port):
		''' Use a socket connection to get server status. '''
		try:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.settimeout(2)
			p1 = time.time()
			s.connect( (address, port) )
			p2 = time.time()
			s.close()
			return ('online', int(round(p2 - p1, 3) * 1000))
		except:
			return ('offline', '---')

	for s in servers:
		# Get previous status from redis
		if not s.has_key('Status'):
			try:
				log = [json.loads(i) for i in r.lrange('log', 0, 0)][0]
				s['Status'] = log['Status']
			except IndexError:
				s['Status'] = 'Unknown'

		# Get cached status from redis
		status = r.get(s['Name'])
		if status:
			s['Source'] = 'Redis'
			s['Log'] = False
			s['Status'] = status

		# Get current status from socket
		else:
			s['Source'] = 'Socket'
			status, s['Ping'] = get_status(s['Address'], s['Port'])
			s['Time'] = arrow.utcnow().to('America/Los_Angeles').format('YYYY-MM-DD HH:mm:ss Z')

			# Status logging
			if s['Status'] != status:
				log = {'Time': s['Time'], 'Name': s['Name'], 'Status': status, 'Ping': s['Ping']}
				r.lpush('log', json.dumps(log))
				s['Log'] = True
			else:
				s['Log'] = False

			# Update status
			r.set(s['Name'], status, settings.CACHE['TTL'])
			s['Status'] = status

	bottle.response.content_type = 'application/json'
	return json.dumps(servers)


@bottle.route('/log', method='GET')
def view_full_log():
	''' Return log html template on GET requests. '''
	logs = [json.loads(i) for i in r.lrange('log', 0, -1)]
	return bottle.template('log', logs=logs)


@bottle.route('/log', method='POST')
def view_log():
	''' Return the log json string on POST requests. '''
	bottle.response.content_type = 'application/json'
	r.ltrim('log', 0, 29)
	return json.dumps([json.loads(i) for i in r.lrange('log', 0, 4)])


if __name__ == '__main__':
	bottle.run(host=settings.BOTTLE['Hostname'],
		port=settings.BOTTLE['Port'],
		server='gevent',
		reloader=settings.BOTTLE['Debug'],
		interval=120
	)
