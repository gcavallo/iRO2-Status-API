#!/usr/bin/env python
# -*- coding: utf-8 -*-

# iRO2-Status-API
# http://github.com/gcavallo/iro2-status-api/

# Copyright (c) 2014 by Gabriel Cavallo <gabrielcavallo@mail.com>
# BSD 3-Clause License http://opensource.org/licenses/BSD-3-Clause


from __future__ import print_function

import gevent; gevent.monkey_patch()
import bottle
import json

import settings
import models


servers = settings.SERVERS
cache = models.Cache(settings.CACHE['Hostname'], settings.CACHE['Port'])
bottle.TEMPLATE_PATH.insert(0, 'templates')
bottle.debug(settings.BOTTLE['Debug'])


@bottle.route('/')
def index():
	''' Return index html template on GET requests. '''
	return bottle.template('index', servers=servers, ttl=settings.CACHE['TTL'])


@bottle.route('/', method='POST')
def view_status():
	''' Return json object on POST requests. '''
	for s in servers:
		status = cache.get(s['Name'])
		if status:
			print('Reading {0} from redis.'.format(s['Name']))
			s['status'] = status
		else:
			server = models.Server(s['Name'], s['Address'], s['Port'])
			status = server.get_status()
			cache.set(s['Name'], status, settings.CACHE['TTL'])
			s['Status'] = status
			print('Reading {0} from socket.'.format(s['Name']))

	bottle.response.content_type = 'application/json'
	return json.dumps(servers)


if __name__ == '__main__':
	bottle.run(host=settings.BOTTLE['Hostname'],
		port=settings.BOTTLE['Port'],
		server='gevent',
		reloader=settings.BOTTLE['Debug'],
		interval=120
	)
