$( document ).ready(function() {
	fetch('/stories/top')
	.then(function (response) {	
		console.log("Got back data");			
		return response.json();
	})
	.then(function (topStories) {		
		var FileDate = topStories[0].FileDate;
		$("#FileDate").append(FileDate);
		renderStories(topStories);

		// Save story data in local Storage
		localStorage['topStories'] = JSON.stringify(topStories); 
		console.log("saved data to local storage");	
		$("#hnLoader").hide();
	})
});

function searchItem() {
	$("#hnLoader").show();			
	var input,filter, txtValue;			
	input = document.getElementById("searchInput");
	filter = input.value.toUpperCase();
	var stories = JSON.parse(localStorage['topStories']);
	if(filter!=""){	
		var storyResult = [];
		$("#searchTableBody").empty();			
		for(var i=0; i<stories.length; i++){
			if(stories[i].title.toUpperCase().indexOf(filter) > -1){
				storyResult.push(stories[i]);									
			}
		}
		renderStories(storyResult);
	}
	else{
		$("#searchTableBody").empty();
		renderStories(stories);
	}	
	$("#hnLoader").hide();			
}

function renderStories(topStories){
	// debugger
	var positive = '<i class="material-icons green-text">sentiment_satisfied_alt</i>';
	
	var negative = '<i class="material-icons red-text">sentiment_very_dissatisfied</i>';
	
	var neutral = '<i class="material-icons grey-text">sentiment_satisfied</i>';
	
	var stories_container = document.getElementById("searchTableBody");
	
	var i = 1;
	var today = new Date()/1000;
	topStories.forEach(item => {
		var story = document.createElement("tr");
		story.className = "story";

		var subtext = document.createElement("tr");
		subtext.className = "subtext";

		if(i>99){
			subtext.appendChild(document.createElement("td"));
			subtext.appendChild(document.createElement("td"));
			subtext.appendChild(document.createElement("td"));
			subtext.appendChild(document.createElement("td"));
		}
		else if(i>9){
			subtext.appendChild(document.createElement("td"));
			subtext.appendChild(document.createElement("td"));
			subtext.appendChild(document.createElement("td"));
		}
		else{
			subtext.appendChild(document.createElement("td"));
			subtext.appendChild(document.createElement("td"));
		}
		var rank = document.createElement("td");
		rank.className = "rank";
		
		var hn_title = document.createElement("td");
		hn_title.className = "hn_title";
		var hn_title_url = document.createElement("a");
		
		var score = document.createElement("td");
		score.className = "score subtext";
		
		var user = document.createElement("td");
		user.className = "user subtext";
		
		var age = document.createElement("td");
		age.className = "age subtext";
		
		var sentiment = document.createElement("td");
		sentiment.className = "sentiment";
		
		rank.innerHTML = i.toString()+".";
		
		hn_title_url.href = item.url;
		hn_title_url.target = "_blank";
		hn_title_url.append(item.title);
		hn_title.append(hn_title_url);
		
		user.innerHTML = 'by '+'<a target="_blank" href="user/'+item.by.toString()+'">'+item.by.toString()+'</a>';
		
		if(item.score==1){
			score.innerHTML = item.score.toString() + " point";
		}
		else{
			score.innerHTML = item.score.toString() + " points";
		}
		
		var age_hours = Math.floor(	(today - topStories[0].time)/(3600)	);
		var age_string = "";
		if(age_hours==1){
			age_string = age_hours.toString() + " hour ago"
		}
		else{
			age_string = age_hours.toString() + " hours ago"
		}
		age.innerHTML = age_string;
		
		if(item.sentiment=="positive"){
			sentiment.innerHTML = positive;
		}
		else if(item.sentiment=="negative"){
			sentiment.innerHTML = negative;
		}
		else{
			sentiment.innerHTML = neutral;
		}
		
		story.appendChild(rank);
		story.appendChild(hn_title);
		subtext.appendChild(score);
		subtext.appendChild(user);
		subtext.appendChild(age);
		story.appendChild(sentiment);
		
		stories_container.appendChild(story);
		stories_container.appendChild(subtext);
		i+=1;
	});
}
