function refresh_log() {
	var xhr = new XMLHttpRequest();
	/* The fetch succeeded. */
	xhr.addEventListener('load', function() {
		/* Clear previous data */
		var c = document.getElementById("log-ajax");
		while (c.lastChild) c.removeChild(c.lastChild);
		/* Parse new data */
		var data = JSON.parse(xhr.responseText);
		console.log("Logs =", data);
		/* Loop through the log objects */
		for (var d in data) {
			/* Create a table row node */
			var logrow_node = document.createElement('tr');
			logrow_node.className = data[d].Status;
			/* Create table column nodes */
			var logtime_node = document.createElement('td');
			var logtime_text = document.createTextNode(data[d].Time);
			logtime_node.appendChild(logtime_text);
			logrow_node.appendChild(logtime_node);
			var logserver_node = document.createElement('td');
			var logserver_text = document.createTextNode(data[d].Name);
			logserver_node.appendChild(logserver_text);
			logrow_node.appendChild(logserver_node);
			var logstatus_node = document.createElement('td');
			var logstatus_text = document.createTextNode(data[d].Status);
			logstatus_node.appendChild(logstatus_text);
			logrow_node.appendChild(logstatus_node);
			var logping_node = document.createElement('td');
			var logping_text = document.createTextNode(data[d].Ping);
			logping_node.appendChild(logping_text);
			logrow_node.appendChild(logping_node);
			/* Append a row to the table */
			document.getElementById("log-ajax").appendChild(logrow_node);
		}
	}, false);
	xhr.open('POST', '/log');
	xhr.timeout = 2000;
	xhr.send();
}

function refresh_status() {
	var xhr = new XMLHttpRequest();
	/* The fetch succeeded. */
	xhr.addEventListener('load', function() {
		/* Clear previous data */
		var c = document.getElementById("status-ajax");
		while (c.lastChild) c.removeChild(c.lastChild);
		/* Parse new data */
		var data = JSON.parse(xhr.responseText);
		console.log("Status =", data);
		var log = false;
		/* Loop through the status objects */
		for (var d in data) {
			/* Create a list item node */
			var list_node = document.createElement('li');
			list_node.id = data[d].Name;
			list_node.className = data[d].Status;
			var list_text = document.createTextNode(data[d].Name + ' is ');
			list_node.appendChild(list_text);
			/* Create a status node */
			var status_node = document.createElement('strong');
			var status_text = document.createTextNode(data[d].Status);
			status_node.appendChild(status_text);
			/* Append a status to a list */
			list_node.appendChild(status_node);
			/* Append a list item to the unordered list */
			document.getElementById("status-ajax").appendChild(list_node);
			if (data[d].Log) log = true;
		}
		if (log) refresh_log();
	}, false);
	xhr.addEventListener('loadend', function() {
		var now = new Date();
		console.info(now.toLocaleString());
		window.setTimeout(refresh_status, 10000);
	}, false);
	xhr.open('POST', '/');
	xhr.timeout = 5000;
	xhr.send();
}
