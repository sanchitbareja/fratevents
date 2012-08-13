
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
				console.log(new Date(data['events'][party_date][1][event]['startTime']))

				// console.log(new Date(data['events'][event]['startTime']*1000+72000000-1));
				// console.log(new Date(data['events'][event]['endTime']*1000+72000000-1));
				//$("#items").append("name:   "+data['friends'][friend]['name']+"    fb_id:   "+data['friends'][friend]['fb_id']+"<br />");
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
				newa.appendChild(document.createTextNode("By "+data['events'][party_date][1][event]['host']+" @ "+(new Date(data['events'][party_date][1][event]['startTime'])).toLocaleTimeString()));
				var newli = document.createElement("li");

				// newli.className = "head";
				newli.appendChild(newa);
				oldul.appendChild(newli);

				attachEventsToMarkers(marker,
					data['events'][party_date][1][event]['id'],
					data['events'][party_date][1][event]['title'],
					data['events'][party_date][1][event]['lat'],
					data['events'][party_date][1][event]['lng'],
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

	function attachEventsToMarkers(marker,rageID,eventName,eventLat,eventLng,numberOfRagers,where,startTime,hostid,host,newli){
		var contentInfo = '<div><p style="text-align:center;">'+eventName+'</p>Host: <a href="javascript:;" onclick=getClubInfo('+hostid+')>'+host+'</a><br/>Time: '+startTime+'<br />Where: '+where+'<br /><br /><br /><div id="rageID_'+rageID+'"><a href="javascript:;" class="rageButton" onclick=sendRageRequest('+rageID+')>&#9996; </a>'+numberOfRagers+' others raged here</div></div>';

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
			newModal = '<div id="club_'+returnData['id']+'" class="reveal-modal"><h1>'+returnData['name']+'</h1><p>'+returnData['description']+'</p><a class="close-reveal-modal">&#215;</a></div>';
			$(newModal).appendTo('body');
			$("#club_"+returnData['id']).reveal();
		}
	});
}

function loadScript() {
	var script = document.createElement("script");
	script.type = "text/javascript";
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
			$('#rageID_'+rageID).replaceWith('DONE RAGING with '+returnData['numberOfRagers']+' others!');
		} else {
			$('#rageID_'+rageID).replaceWith('DONE RAGING!');
		}
	});
}

window.onload = loadScript;