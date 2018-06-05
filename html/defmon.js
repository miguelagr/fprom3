function loadD() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) { 
      var para = document.createElement("p");
	var node = document.createElementNS(this.responseText);
	para.appendChild(node);
	var element = document.getElementById("demo");
	element.appendChild(para);
    }
  };
  xhttp.open("GET", "tcharts.php", true);
  xhttp.send();
}

function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) { 
	var element = document.getElementById("mbody").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "dominios.php", true);
  xhttp.send();
}

function loadDoc1() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) { 
	var element = document.getElementById("mbody").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "fchart.html", true);
  xhttp.send();
}

function loadDoc4() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) { 
	var element = document.getElementById("mbody").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "clasificacion.php", true);
  xhttp.send();
}


