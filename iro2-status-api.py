#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# iRO2-Status-API
# http://github.com/gcavallo/iro2-status-api/

# Copyright (c) 2014 by Gabriel Cavallo <gabrielcavallo@mail.com>
# BSD 3-Clause License http://opensource.org/licenses/BSD-3-Clause


import json, socket
from datetime import datetime

import redis, bottle
from pytz import timezone
from gevent import monkey; monkey.patch_all()

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
			s.connect( (address, port) )
			s.close()
			return 'online'
		except:
			return 'offline'

	for s in servers:
		# Get previous status from redis
		if not s.has_key('Status'):
			try:
				log = [json.loads(i) for i in r.lrange('log', 0, 0)][0]
				s['Status'] = log['Status']
			except IndexError:
				s['Status'] = 'unknown'

		# Get cached status from redis
		status = r.get(s['Name'])
		if status:
			s['Source'] = 'Redis'
			s['Log'] = False
			s['Status'] = status

		# Get current status from socket
		else:
			s['Source'] = 'Socket'
			status = get_status(s['Address'], s['Port'])
			timestamp = datetime.now(timezone('UTC')).astimezone(timezone('America/Los_Angeles'))
			s['Time'] = timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")

			# Status logging
			if s['Status'] != status:
				log = {'Time': s['Time'], 'Name': s['Name'], 'Status': status}
				r.lpush('log', json.dumps(log))
				r.ltrim('log', 0, 29)
				s['Log'] = True
			else:
				s['Log'] = False

			# Update status
			r.set(s['Name'], status, settings.CACHE['TTL'])
			s['Status'] = status

	bottle.response.content_type = 'application/json'
	bottle.response.set_header('Access-Control-Allow-Origin', '*')
	return json.dumps(servers)


@bottle.route('/log', method='GET')
def view_full_log():
	''' Return log html template on GET requests. '''
	logs = [json.loads(i) for i in r.lrange('log', 0, -1)]
	return bottle.template('log', logs=logs)


@bottle.route('/api', method='GET')
def view_full_log():
	''' Return api html template on GET requests. '''
	return bottle.template('api')


if settings.BOTTLE['Debug']:
	@bottle.route('/static/<filename>')
	def server_static(filename):
		return bottle.static_file(filename, root='./static/')


if __name__ == '__main__':
	bottle.run(host=settings.BOTTLE['Hostname'],
		port=settings.BOTTLE['Port'],
		server='gevent',
		reloader=settings.BOTTLE['Debug'],
		interval=120
	)
