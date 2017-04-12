var viewport = document.getElementById('viewport');
var buttonTray = document.getElementById('buttonTray');
function addCard (name) {
  var doc = document;
  var ele = doc.createElement('div');
  switch (name) {
    case 0:
      ele.id = "introName";
      ele.innerHTML = '<div class="tooltip">What\'s your name?</div><input id="introName_text" type="text"/>';
      break;
  }
}

function setCalTo (mm, yyyy) {
  var currMonthDeeds = getMonthDetails(mm, yyyy);
  document.getElementById('classes_calendar_month').innerHTML = currMonthDeeds[0];
  var dates = document.getElementById('classes_calendar_dates');
  dates.innerHTML = "";
  var doc = document;
  var date_length = currMonthDeeds[1] + currMonthDeeds[2];
  if (currMonthDeeds[2] === 0) {
    currMonthDeeds[2] = 7;
  }
  var tr = doc.createElement('tr');
  var flag = true;
  for (var i = 1; i < date_length; i++) {
    var td = doc.createElement('td');
    if ((i - currMonthDeeds[2] + 1) > 0) {
      td.innerHTML = (i - currMonthDeeds[2] + 1);
      var inp = doc.createElement('input');
      inp.type = "hidden";
      var dd__ = (i - currMonthDeeds[2] + 1);
      if (dd__ < 10) {
        dd__ = "0" + dd__;
      }
      else {
        dd__ = "" + dd__;
      }
      inp.value = currMonthDeeds[3] + "-" + currMonthDeeds[4] + "-" + dd__;
      td.appendChild(inp);
      td.addEventListener('click', function () {
        if (this.className !== "selected") {
          selectDate(this);
        }
      }, false);
      if (flag) {
        selectDate(td);
        flag = false;
      }
    }
    else {
      td.innerHTML = "--";
    }
    tr.appendChild(td);
    if (i % 7 === 0) {
      dates.appendChild(tr);
      tr = doc.createElement('tr');
    }
  }
  dates.appendChild(tr);
};
function getMonthDetails (month, year) {
  var details = [];
  var m = 0;
  switch (month) {
    case 0:
      details = ["January, " + year, 31];
      m = 11;
      break;
    case 1:
      if (year % 4 === 0) {
        details = ["Febuary, " + year, 29];
      }
      else {
        details = ["Febuary, " + year, 28];
      }
      m = 12;
      break;
    case 2:
      details = ["March, " + year, 31];
      m = 1;
      break;
    case 3:
      details = ["April, " + year, 30];
      m = 2;
      break;
    case 4:
      details = ["May, " + year, 31];
      m = 3;
      break;
    case 5:
      details = ["June, " + year, 30];
      m = 4;
      break;
    case 6:
      details = ["July, " + year, 31];
      m = 5;
      break;
    case 7:
      details = ["August, " + year, 31];
      m = 6;
      break;
    case 8:
      details = ["September, " + year, 30];
      m = 7;
      break;
    case 9:
      details = ["October, " + year, 31];
      m = 8;
      break;
    case 10:
      details = ["November, " + year, 30];
      m = 9;
      break;
    case 11:
      details = ["Decemeber, " + year, 31];
      m = 10;
      break;
  }
  var _year = "" + year;
  _year.split('');
  var _D = parseInt(_year[2] + _year[3]);
  var _C = parseInt(_year[0] + _year[1]);
  day = 1 + Math.floor(((13 * m) - 1) / 5) + _D + Math.floor(_D / 4) + Math.floor(_C / 4) - 2 * _C;
  if (day < 0) {
    day = (day % 7) + 7;
  }
  else {
    day = day % 7;
  }
  details.push(day);
  details.push(year);
  var month_ =  month + 1;
  if (month_ < 10) {
    month_ = "0" + month_;
  }
  else {
    month_ += "";
  }
  details.push(month_);
  return details;
};
function selectDate (obj) {
  if (currSelection !== undefined) {
    currSelection.className = "";
  }
  obj.className = "selected";
  currSelection = obj;
  updateClasses(obj.querySelector("input[type=hidden]").value, document.getElementById('year_years_selection').value, document.getElementById('batch_batches_selection').value);
};
function updateClasses (date, year, batch) {
  console.log("/classdata?date=" + date + "&batch=" + year + "+Year+Batch+" + batch);
  var xmlhttp;
  if (window.XMLHttpRequest) {
    xhttp = new XMLHttpRequest();
  } else {
    // code for older browsers
    xhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      // TODO
    }
  };
  xhttp.open("GET", "/classdata?date=" + date + "&batch=" + year + "+Year+Batch+" + batch, true);
  //xhttp.send();
}
function harvest () {
  var details = {};
  details.name = "" + document.getElementById('name_text').value;
  details.rollNumber = "" + document.getElementById('number_number').value;
  details.year = "" + document.getElementById('year_years_selection').value;
  details.batch = "" + document.getElementById('batch_batches_selection').value;
  details.selectedClasses = [];
  details.event = "" + document.getElementById('events_text').value;
  return details;
};

document.getElementById('classes_calendar_prev').addEventListener('click', function () {
  mm--;
  if (mm < 0) {
    mm = 11;
    yyyy--;
  }
  setCalTo(mm, yyyy);
}, false);
document.getElementById('classes_calendar_next').addEventListener('click', function () {
  mm++;
  if (mm >= 11) {
    mm = 0;
    yyyy++;
  }
  setCalTo(mm, yyyy);
}, false);
document.getElementById('classes_calendar_today').addEventListener('click', function () {
  var d = new Date();
  var mm = d.getMonth();
  var yyyy = d.getFullYear();
  setCalTo(mm, yyyy);
}, false);

var eles = document.querySelectorAll('.radio');
var eles_length = eles.length;
for (var i = 0; i < eles_length; i++) {
  var eles_divs = eles[i].querySelectorAll('div');
  var eles_divs_length = eles_divs.length;
  var flag = true;
  for (var j = 0; j < eles_divs_length; j++) {
    if (flag) {
      eles_divs[j].parentNode.querySelector('input').value = eles_divs[j].textContent;
      eles_divs[j].className = 'selected';
      flag = false;
    }
    eles_divs[j].addEventListener('click', function () {
      this.parentNode.querySelector('input').value = this.textContent;
      this.parentNode.querySelector('.selected').className = '';
      this.className = 'selected';
      updateClasses(document.getElementById("classes_calendar_dates").querySelector("td.selected").querySelector("input[type=hidden]").value, document.getElementById('year_years_selection').value, document.getElementById('batch_batches_selection').value);
    }, false);
  }
}

var d = new Date();
var mm = d.getMonth();
var yyyy = d.getFullYear();
var currSelection;
setCalTo(mm, yyyy);
