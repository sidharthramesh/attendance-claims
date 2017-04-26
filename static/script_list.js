function parse_ (claims) {
  var len = claims.length;
  for (var i = 0; i < len; i++) {
    toTree(claims[i]);
  }
};
var Tree = [];
if (TreeMeta) {
  var TreeMeta = {
    _1Data: {
      name: "",
      rollNo: 0
    },
    _2Data: {}
  };
  function toTree (claimObj) {
    if (claimObj) {
      
    }
  };
}

function createFirstCard (title, info, list) {
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
  if (list) {
    var list_length = list.length;
    for (var i = 0; i < list_length; i++) {
      var item = list[i];
      ele.appendChild(createSecondCard(item.title, item.info, item.list));
    }
  }
  return ele;
};
function createSecondCard (title, info, list) {
  var ele = document.createElement('div');
  ele.className = "second";
  var title_ = document.createElement('h2');
  title_.textContent = title;
  ele.appendChild(title_);
  if (info) {
    var info_ = document.createElement('div');
    info_.className = "info";
    info_.innerHTML = info.join('<br/>');
    ele.appendChild(info_);
  }
  if (list) {
    var list_length = list.length;
    for (var i = 0; i < list_length; i++) {
      var item = list[i];
      //ele.appendChild(createThirdCard(item.title, item.info, item.list));
    }
  }
  return ele;
};

// On xhttp sucess
var xmlhttp = new XMLHttpRequest();
xmlhttp.open("GET", '/claims');
xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    if (this.responseText) {
      //document.getElementById('claims').innerHTML = "";
      var claims = JSON.parse(this.responseText);
      if (claims instanceof Array) {
        parse_(claims);
      }
      else if (claims instanceof Object) {
        parse(claims);
      }
    }
    else {}
  }
};
xmlhttp.send();
