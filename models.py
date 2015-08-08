# -*- coding: utf-8 -*-

# iRO2-Status-API
# http://github.com/gcavallo/iro2-status-api/

# Copyright (c) 2014 by Gabriel Cavallo <gabrielcavallo@mail.com>
# BSD 3-Clause License http://opensource.org/licenses/BSD-3-Clause


import redis
import socket


class Cache(object):
	'''
	Redis server model.

	:param str hostname: Address of the Redis server.
	:param integer port: Port of the Redis server.
	'''
	def __init__(self, hostname='127.0.0.1', port=6379):
		self.server = redis.Redis(hostname, port)

	def set(self, key, value, ttl=60):
		'''
		Set the value at `key` to `value` and set an
		expire flag on `key` for `ttl` seconds.

		:param str key: Name of the Redis key.
		:param str value: Value associated to the Redis key.
		:param integer ttl: Time to live in seconds before the key expires.
		'''
		self.server.set(key, value, ttl)

	def get(self, key):
		'''
		Return the value at `key`, or None if the key doesn't exist.

		:param str key: Name of the Redis key.
		:return: Value associated to the Redis key.
		:rtype: str
		'''
		return self.server.get(key)

	def delete(self, *keys):
		'''
		Delete one or more keys specified by `*keys`.

		:param str *keys: Name of the Redis keys to be deleted.
		'''
		self.server.delete(keys)


class Server(object):
	'''
	iRO2 server model.

	:param str name: Name of the Ragnarok Online 2 server.
	:param str address: Address of the Ragnarok Online 2 server.
	:param int port: Port of the Ragnarok Online 2 server.
	'''
	def __init__(self, name, address, port):
		self.name = name
		self.address = address
		self.port = port

	def get_status(self):
		'''
		Use a socket connection to get server status.
		The server is considered offline after a 3 second timeout.

		:return: Status of the server as "online" or "offline".
		:rtype: str
		'''
		try:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.settimeout(3)
			s.connect( (self.address, self.port) )
			s.close()
			return 'online'
		except:
			return 'offline'
