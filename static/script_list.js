function parse (claims) {
  var len = claims.length;
  var main = createFirstCard(claims[0].Name, [
    'Roll Number: ' + claims[0].Roll_no,
    'Serial Number: ' + claims[0].Serial
  ]);
  var eventsIds = [];
  var events = [];
  for (var i = 0; i < len; i++) {
    var index = eventsIds.indexOf(claims[i].Event);
    if (index === -1) {
      index = eventsIds.length;
      eventsIds[index] = claims[i].Event;
      events[index] = [];
    }
    events[index].push(claims[i]);
  }
  var events_length = events.length;
  for (var i = 0; i < events_length; i++) {
    var events_ = createSecondCard(eventsIds[i], []);
    var event = events[i];
    var event_length = event.length;
    for (var j = 0; j < event_length; j++) {
      var event_ = createClaimCard(event[j]);
      events_.appendChild(event_);
    }
    main.appendChild(events_);
  }
  document.getElementById('claims').appendChild(main);
};


function createFirstCard (title, info) {
  var ele = document.createElement('div');
  ele.className = "first";
  var title_ = document.createElement('h2');
  title_.textContent = title;
  ele.appendChild(title_);
  if (info) {
    var info_ = document.createElement('div');
    info_.className = "info";
    info_.innerHTML = info.join('<br/>');
    ele.appendChild(info_);
  }
  return ele;
};
function createSecondCard (title, info, list) {
  var ele = document.createElement('div');
  ele.className = "second";
  var title_ = document.createElement('h3');
  title_.textContent = title;
  ele.appendChild(title_);
  if (info) {
    var info_ = document.createElement('div');
    info_.className = "info";
    info_.innerHTML = info.join('<br/>');
    ele.appendChild(info_);
  }
  return ele;
};
function createClaimCard (claim) {
  var title = claim.Period,
  date = claim.Date.substring(0,16),
  time = claim.Time,
  id = claim.id,
  disapproved = claim.dissapproved,
  status = claim.status;
  var ele = document.createElement('div');
  ele.className = "claimCard";
  var txt = '<div><h4>CLASS_NAME</h4><div><span>DATE</span><br/><span>TIME</span></div></div><div><img/><img/><img/><input type="hidden"/>';
  txt = txt.replace('CLASS_NAME', title);
  txt = txt.replace('DATE', date);
  txt = txt.replace('TIME', time);
  ele.innerHTML = txt;
  ele.querySelector('input').value = id;
  var yes = '/static/approved.png';
  var no = '/static/unseen.png';
  console.log(claim);
  if (disapproved === 1) {
    no = '/static/disapproved.png';
  }
  if (status.js === 1) {
    ele.querySelector('img:nth-child(1)').src = yes;
  }
  else {
    ele.querySelector('img:nth-child(1)').src = no;
  }
  if (status.office === 1) {
    ele.querySelector('img:nth-child(2)').src = yes;
  }
  else {
    ele.querySelector('img:nth-child(2)').src = no;
  }
  if (status.dept === 1) {
    ele.querySelector('img:nth-child(3)').src = yes;
  }
  else {
    ele.querySelector('img:nth-child(3)').src = no;
  }
  return ele;
};

window.addEventListener('load', function () {
  // On xhttp sucess
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", '/claims');
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      if (this.responseText) {
        document.getElementById('claims').innerHTML = "";
        var claims = JSON.parse(this.responseText);
        parse(claims);
      }
      else {}
    }
  };
  xmlhttp.send();
}, false);

document.getElementById('buttonTray_logout').addEventListener('click', function () {
  window.location.href = "/logout";
});
