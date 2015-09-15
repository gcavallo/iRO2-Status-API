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
		}
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
