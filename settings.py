# -*- coding: utf-8 -*-

# iRO2-Status-API
# http://github.com/gcavallo/iro2-status-api/

# Copyright (c) 2014 by Gabriel Cavallo <gabrielcavallo@mail.com>
# BSD 3-Clause License http://opensource.org/licenses/BSD-3-Clause


# iRO2 servers.
SERVERS = [
	{
		'Name': 'Patch',
		'Address': 'patch.playragnarok2.com',
		'Port': 80
	},
	{
		'Name': 'Login',
		'Address': 'login.playragnarok2.com',
		'Port': 7101
	},
	{
		'Name': 'Odin',
		'Address': '128.241.94.47',
		'Port': 7204
	}
]


# Redis server.
CACHE = {
	'Hostname': '127.0.0.1',
	'Port': 6379,
	'TTL': 30
}


# Bottle server.
BOTTLE = {
	'Debug': False,
	'Hostname': '127.0.0.1',
	'Port': 12000
}
