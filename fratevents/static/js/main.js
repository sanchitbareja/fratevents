
var map;

function initialize() {
  	var mapCenter = new google.maps.LatLng(37.87201, -122.25775);		
	var mapOptions = {
	    zoom: 15,
	    mapTypeId: google.maps.MapTypeId.ROADMAP,
	    center: mapCenter
	};
	
	var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

	//get all the events from the database
	$.get('get/events/',function(data){
		console.log(data);
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

				//Add into sidebar list
				var oldul = document.querySelectorAll("#nlists")[0];
				var newa = document.createElement("a");
				newa.className = "eventInformation";
				var eventTitle = document.createElement("p");
				eventTitle.className = "eventTitle";
				eventTitle.appendChild(document.createTextNode(marker.getTitle()));
				newa.appendChild(eventTitle);
				newa.appendChild(document.createTextNode("By "+data['events'][party_date][1][event]['host']+", @"+data['events'][party_date][1][event]['host']+", "+formatAMPM(new Date(data['events'][party_date][1][event]['startTime']))));
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
	});
	/* FOR SCROLL EFFECTS */
	var lists = document.querySelectorAll('#nlists ul');

	function attachEventsToMarkers(marker,rageID,eventName,eventDescription,image,numberOfRagers,where,startTime,hostid,host,newli){
		var contentInfo = '<div id="markerContentInfo"><div id="markerContentHeader"><img id="markerContentImage" src="'+image+'" /><div id="markerContentHeaderText">'+eventName+', <a href="javascript:;" onclick=getClubInfo('+hostid+')>'+host+'</a></div></div><br/><div id="markerContentWhereWhen">@ '+where+', '+formatAMPM(new Date(startTime))+'</div><div id="markerContentMainText">'+eventDescription+'</div><div class="rageContainer"><div id="rageID_'+rageID+'"><a href="javascript:;" class="rageButton" onclick=sendRageRequest('+rageID+')>&#9996; </a>'+numberOfRagers+' others raged here</div></div></div>';

		var infowindow = new google.maps.InfoWindow({
		    content: contentInfo,
		    maxWidth: 500
		});

		//handling what happens when marker is clicked
		function toggleClick() {
			if(infowindow.getMap()){
				infowindow.close();				
			} else {
				infowindow.open(map,marker);
			}
		}

		function toggleBounce() {
			if(marker.getAnimation() == null){
				marker.setAnimation(google.maps.Animation.BOUNCE);
			} else {
				marker.setAnimation(null);
			}
		}

		//add listner to the marker
		google.maps.event.addListener(marker, 'click', function(){ infowindow.open(map,marker); });

		//attaching events to list items in sidebar
		google.maps.event.addDomListener(newli,'click', toggleClick);
		google.maps.event.addDomListener(newli,'mouseover', toggleBounce);
		google.maps.event.addDomListener(newli,'mouseout', toggleBounce);

	}
}

function getClubInfo(hostid){
	console.log(hostid);
	$.ajax({
		type: "POST",
		url: "/frat/",
		data: { clubID: hostid, csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() }
	}).done(function(returnData){
		if(returnData['success']){
			console.log(returnData);
			newModal = '<div id="club_'+returnData['id']+'" class="reveal-modal expand"><div id="clubInfoHeader"><img id="clubInfoHeaderImage" src="'+returnData['image']+'" /><h1 id="clubInfoHeaderText">'+returnData['name']+'</h1></div><div id="clubInfoBody"><b><i>Founded in '+returnData['founded']+'</i></b><p><b><i>Type of Organization: '+returnData["typeOfOrganization"]+'</i></b></p><p>'+returnData['description']+'</p></div><a class="close-reveal-modal">&#215;</a></div>';
			$(newModal).appendTo('body');
			$("#club_"+returnData['id']).reveal();
		}
	});
}

function loadScript() {
	$(this).joyride({
		'cookieMonster': true,           // true/false for whether cookies are used
		  'cookieName': 'JoyRide',         // choose your own cookie name
		  'cookieDomain': 'calhaps.com',           // set to false or yoursite.com
	});
	var script = document.createElement("script");
	script.type = "text/javascript";
	//the callback function is initialize()
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
	strTime = hours + ':' + minutes + ' ' + ampm;
	return strTime;
}

window.onload = loadScript;
