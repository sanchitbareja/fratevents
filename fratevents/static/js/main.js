
var map;
var mapCenter;
var mapOptions;
var markers = [];

function initialize() {
	//import infobox.js --need to load synchronously
  	var infoboxScript = document.createElement("script");
  	infoboxScript.type = "text/javascript";
  	infoboxScript.src = "http://google-maps-utility-library-v3.googlecode.com/svn/tags/infobox/1.1.9/src/infobox.js";
  	document.body.appendChild(infoboxScript);
  	infoboxScript.onload = initializeMarkers;
  	getFilters();
}

function initializeMarkers() {

  	mapCenter = new google.maps.LatLng(37.87201, -122.25775);		
	mapOptions = {
	    zoom: 15,
	    mapTypeId: google.maps.MapTypeId.ROADMAP,
	    center: mapCenter
	};
	
	map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

	//get all the events from the database
	$.ajax({
		type: "POST",
		url: "/get/events/",
		data: { csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() }
	}).done(function(data){
		if(data['success']){
			//add coordinates to list and add markers + map formatting
			for(var party_date in data['events']){
				//Add into sidebar list
				var oldul = document.querySelectorAll("#nlists")[0];
				var newli = document.createElement("li");

				eventDate = new Date(data['events'][party_date][0]);
				newli.className = "head";
				newli.appendChild(document.createTextNode(eventDate.toDateString()));
				newli.id = eventDate.getUTCDate() + "" + eventDate.getUTCMonth() + "" + eventDate.getUTCFullYear();
				oldul.appendChild(newli);

				for(var event in data['events'][party_date][1]){
					var newMarkerPos = new google.maps.LatLng(data['events'][party_date][1][event]['lat'],data['events'][party_date][1][event]['lng']);
					var marker = new google.maps.Marker({
					    map:map,
					    draggable:false,
					    animation: google.maps.Animation.DROP,
					    position: newMarkerPos,
					    title:data['events'][party_date][1][event]['title']
					});

					markers.push(marker);

					//Add into sidebar list
					var oldul = document.querySelectorAll("#nlists")[0];
					var newa = document.createElement("a");
					newa.className = "eventInformation";
					var eventTitle = document.createElement("p");
					eventTitle.className = "eventTitle";
					eventTitle.appendChild(document.createTextNode(marker.getTitle()));
					newa.appendChild(eventTitle);
					newa.appendChild(document.createTextNode("By "+data['events'][party_date][1][event]['host']+", @"+data['events'][party_date][1][event]['where']+", "+formatAMPM(new Date(data['events'][party_date][1][event]['startTime']))));
					var newli = document.createElement("li");
					if(event == 0){
						newli.id = "eventTour";
					}

					// newli.className = "head";
					newli.appendChild(newa);
					oldul.appendChild(newli);

					attachEventsToMarkers(marker,
						data['events'][party_date][1][event]['id'],
						data['events'][party_date][1][event]['title'],
						data['events'][party_date][1][event]['eventDescription'],
						data['events'][party_date][1][event]['image'],
						data['events'][party_date][1][event]['numberOfRagers'],
						data['events'][party_date][1][event]['where'],
						data['events'][party_date][1][event]['startTime'],
						data['events'][party_date][1][event]['hostid'],
						data['events'][party_date][1][event]['host'],
						newli);
				}
			}
		}
	});

	/* FOR SCROLL EFFECTS */
	var lists = document.querySelectorAll('#nlists ul');

}

function attachEventsToMarkers(marker,eventID,eventName,eventDescription,image,numberOfRagers,where,startTime,hostid,host,newli){
	var contentInfo = 	'<div id="markerContentInfo"><div id="tipBox"></div>'+
							'<div id="markerContentHeader">'+
								'<div id="markerContentHeaderText">'+eventName+
									', <a href="javascript:;" onclick=getClubInfo('+hostid+')>'+host+'</a>'+
								'</div>'+
							'</div>'+
							'<br/><div id="markerContentWhereWhenDiv">'+
							'<p class="radius success label" id="markerContentWhereWhenText">@ '+where+', '+formatAMPM(new Date(startTime))+'</p>'+
							'<br /></div>'+
							'<div id="markerContentMainText">'+
								'<img id="markerContentImage" src="'+image+'" />'+
								'<p>'+eventDescription+'</p><p id="eventLink">&hellip;<a href="/event/'+eventID+'" target="_blank"/>More on the event</a>'+
							'</div>'+
							'<div class="rageContainer">'+
								'<div id="rageID_'+eventID+'">'+
									'<a href="javascript:;" class="rageButton" onclick=sendRageRequest('+eventID+')>&#9996; </a>'+
									numberOfRagers+' others raged here'+
								'</div>'+
							'</div>'+
						'</div>';

	//handling what happens when marker is clicked
	function toggleClick() {
		if(ib.getMap()){
			ib.close();				
		} else {
			ib.open(map,marker);
		}
	}

	function toggleBounce() {
		if(marker.getAnimation() == null){
			marker.setAnimation(google.maps.Animation.BOUNCE);
		} else {
			marker.setAnimation(null);
		}
	}

	var myOptions = {
		 content: contentInfo
		,pixelOffset: new google.maps.Size(-160, 0)
		,boxStyle: {
			width:"400px",
			height:"230px",
			opacity: 1.0
		}
		,disableAutoPan: false
		,maxWidth: 500
		,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
		,infoBoxClearance: new google.maps.Size(100, 100)
		,isHidden: false
		,pane: "floatPane"
		,enableEventPropagation: true
	};

	var ib = new InfoBox(myOptions);

	//add listener to the marker
	google.maps.event.addListener(marker, "click", toggleClick);
	//attaching events to list items in sidebar
	google.maps.event.addDomListener(newli,'click', toggleClick);
	google.maps.event.addDomListener(newli,'mouseover', toggleBounce);
	google.maps.event.addDomListener(newli,'mouseout', toggleBounce);
}

function getFilters(){
	$.ajax({
		type: "POST",
		url: "/get/filters/",
		data: { csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() }
	}).done(function(returnData){
		if(returnData['success']){
			for (var key in returnData['filters']) {
				if(returnData['filters'][key] == 0){
					$("#filter-submenu").append('<li id="filter-submenu-content"><a href="javascript:;" onclick=getFilteredEvents("'+key+'")><span class="radius secondary label">'+key+'</span></a></li>');
				} else {
					$("#filter-submenu").append('<li id="filter-submenu-content"><a href="javascript:;" onclick=getFilteredEvents("'+key+'")><span class="radius label">'+key+'</span></a></li>');
				}
			};
		}
	});
}

function getFilteredEvents(filter_text){
	$.ajax({
		type: "POST",
		url: "/get/filters/"+filter_text+"/",
		data: { csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() }
	}).done(function(returnData){
		if(returnData["success"]){
			//remove existing markers and lists
			for (var i = markers.length - 1; i >= 0; i--) {
				markers[i].setMap(null);
			};
			$("#nlists").children().remove();

			//reset the filter-submenu-header
			$("#filter-submenu-header").text(filter_text);

			//add the new lists
			//add coordinates to list and add markers + map formatting
			for(var party_date in returnData['events']){
				//Add into sidebar list
				var oldul = document.querySelectorAll("#nlists")[0];
				var newli = document.createElement("li");

				eventDate = new Date(returnData['events'][party_date][0]);
				newli.className = "head";
				newli.appendChild(document.createTextNode(eventDate.toDateString()));
				newli.id = eventDate.getUTCDate() + "" + eventDate.getUTCMonth() + "" + eventDate.getUTCFullYear();
				oldul.appendChild(newli);

				for(var event in returnData['events'][party_date][1]){
					var newMarkerPos = new google.maps.LatLng(returnData['events'][party_date][1][event]['lat'],returnData['events'][party_date][1][event]['lng']);
					var marker = new google.maps.Marker({
					    map:map,
					    draggable:false,
					    animation: google.maps.Animation.DROP,
					    position: newMarkerPos,
					    title:returnData['events'][party_date][1][event]['title']
					});

					markers.push(marker);

					//Add into sidebar list
					var oldul = document.querySelectorAll("#nlists")[0];
					var newa = document.createElement("a");
					newa.className = "eventInformation";
					var eventTitle = document.createElement("p");
					eventTitle.className = "eventTitle";
					eventTitle.appendChild(document.createTextNode(marker.getTitle()));
					newa.appendChild(eventTitle);
					newa.appendChild(document.createTextNode("By "+returnData['events'][party_date][1][event]['host']+", @"+returnData['events'][party_date][1][event]['where']+", "+formatAMPM(new Date(returnData['events'][party_date][1][event]['startTime']))));
					var newli = document.createElement("li");
					if(event == 0){
						newli.id = "eventTour";
					}

					// newli.className = "head";
					newli.appendChild(newa);
					oldul.appendChild(newli);

					attachEventsToMarkers(marker,
						returnData['events'][party_date][1][event]['id'],
						returnData['events'][party_date][1][event]['title'],
						returnData['events'][party_date][1][event]['eventDescription'],
						returnData['events'][party_date][1][event]['image'],
						returnData['events'][party_date][1][event]['numberOfRagers'],
						returnData['events'][party_date][1][event]['where'],
						returnData['events'][party_date][1][event]['startTime'],
						returnData['events'][party_date][1][event]['hostid'],
						returnData['events'][party_date][1][event]['host'],
						newli);
				}
			}

		}
	});
}

function getClubInfo(hostid){
	$.ajax({
		type: "POST",
		url: "/get/club/",
		data: { clubID: hostid, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() }
	}).done(function(returnData){
		if(returnData['success']){
			newModal = '<div id="club_'+returnData['id']+'" class="reveal-modal expand"><div id="clubInfoHeader"><img id="clubInfoHeaderImage" src="'+returnData['image']+'" /><h1 id="clubInfoHeaderText">'+returnData['name']+'</h1></div><div id="clubInfoBody"><b><i>Founded in '+returnData['founded']+'</i></b><p><b><i>Type of Organization: '+returnData["typeOfOrganization"]+'</i></b></p><p>'+returnData['description']+'</p></div><a class="close-reveal-modal">&#215;</a></div>';
			$(newModal).appendTo('body');
			$("#club_"+returnData['id']).reveal();
		}
	});
}

function loadScript() {
	var script = document.createElement("script");
	script.type = "text/javascript";
	//import google maps with the callback function as initialize()
	script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyD8tgnC9UWlAbebHZm7iHBMH_8B2bd1ork&sensor=true&callback=initialize";
  	document.body.appendChild(script);
}

function sendRageRequest(rageID){
	$.ajax({
		type: "POST",
		url: "/rage/",
		data: { id: rageID, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() }
	}).done(function( returnData ) {
		if(returnData['success']){
			$('#rageID_'+rageID).replaceWith('<div style="font-size:2em; display:inline; color:red;">&#9996;</div> RAGED with '+returnData['numberOfRagers']+' others!');
		} else {
			$('#rageID_'+rageID).replaceWith('RAGED!');
		}
	});
}

function formatAMPM(date) {
	var hours = date.getHours();
	var minutes = date.getMinutes();
	var ampm = hours >= 12 ? 'pm' : 'am';
	var hours = hours % 12;
	hours = hours ? hours : 12; // the hour '0' should be '12'
	minutes = minutes < 10 ? '0'+minutes : minutes;
	day = date.getDate();
	month = date.getMonth() + 1;
	strTime = month+"/"+day+", "+hours + ':' + minutes + ' ' + ampm;
	return strTime;
}

window.onload = loadScript;
