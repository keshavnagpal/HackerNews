$( document ).ready(function() {
	var userid = $("#user_id").text();
	var user_url = "/userdata/"+userid;
	fetch(user_url)
	.then(function (response) {	
		console.log("Got back data");			
		return response.json();
	})
	.then(function (user) {		
		renderUser(user);
		$("#hnLoader").hide();
	})
});

function renderUser(user){
	$("#user_about").html(user.about);
	$("#user_karma").text(user.karma);
	$("#user_created").text((new Date(user.created*1000)).toDateString());
}