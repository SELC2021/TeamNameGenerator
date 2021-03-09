array = [document.getElementById("project1"), document.getElementById("project2"), document.getElementById("project3"), document.getElementById("project4"), document.getElementById("project5")];

function carousel(){
	alert("hello")
	for (i=0, i<array.length(), i++){
		array[i].style.left-=310;
	}
}