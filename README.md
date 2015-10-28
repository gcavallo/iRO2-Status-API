iRO2-Status-API
===============

API to check the status of the official Ragnarok Online 2 servers.

API
---

iRO2-Status-API features a simple and open json api to add the Ragnarok Online 2 server status into your own projects! Some basic knowledge of json and scripting is all you need to get started.

To start using the API, do a POST request at http://status.niceboat-guild.com and parse the json string. The output should look like this:

```json
[{"Status": "online", "Name": "Patch", "Address":"patch.playragnarok2.com", "Source": "Redis", "Time": "2015-09-15 16:11:18 PDT", "Port": 80, "Log": false},
{"Status": "online", "Name": "Login", "Address": "login.playragnarok2.com", "Source": "Redis", "Time": "2015-09-15 16:11:19 PDT", "Port": 7101, "Log": false},
{"Status": "online", "Name": "Odin", "Address": "128.241.94.47", "Source": "Redis", "Time": "2015-09-15 16:11:19 PDT", "Port": 7204, "Log": false}]
```

Each server has its own object containing:

Key         | Type      | Value
:---------- | :-------- | :----
**Status**  | *string*  | "online" or "offline".
**Name**    | *string*  | name of the server.
**Address** | *string*  | IP/DNS address of the server.
**Source**  | *string*  | "Redis" cache or new "Socket".
**Time**    | *string*  | time of the last socket status.
**Port**    | *integer* | port of the server.
**Log**     | *boolean* | if a status change is logged.

Install
-------
For more advanced users, you can deploy the API on your own server to avoid polling http://status.niceboat-guild.com. You will need your own server running the iRO2-Status-API source code, freely available under the BSD 3-clause license.

```sh
git clone https://github.com/gcavallo/iRO2-Status-API.git iRO2-Status-API
```

Configure the api by editing the `settings.py` file. Enable debug for development and make sure to disable it for production!

For deployment, you will need a *service* to run `iro2-status-api.py` at boot, and an *HTTP server* to proxy static files.

Dependencies
------------

* python == 2.7
* python-bottle >= 0.12
* python-redis
* python-pytz
* python-gevent
* redis-server
