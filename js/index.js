function butClick(){
  url='https://shopifyorder.herokuapp.com/orders';
  var e = document.getElementById("cust_list");
  var shopName = e.options[e.selectedIndex].value;
  var finalUrl=url+'?name='+shopName;
  alert(finalUrl);
  $.ajax({
    url: finalUrl,
    type: 'GET',
    success: function (data) {
      alert("success");
      csv = 'data:text/csv;charset=utf-8,' + encodeURI(data);
      link = document.createElement('a');
      link.setAttribute('href', csv);
      link.setAttribute('download', "download.csv");
      link.click()
    },
    error: function(jqxhr, status, exception) {
        alert('Exception:', exception);
    }
  });
}

function createAccount(){
  url='https://shopifyorder.herokuapp.com/createAccount';
  var name = document.getElementById("name").value;
  var email = document.getElementById("email").value;
  var apikey = document.getElementById("apikey").value;
  var password = document.getElementById("password").value;
  var shared = document.getElementById("sharedsecret").value;

  $.ajax({
    url: url,
    type: 'GET',
    data: {name:name,email:email,apikey:apikey,password:password,sharedsecret:shared},
    complete: function(data, status) {
      alert("Account created");
    }
  });
  return false;
}

function getShops(){
  var select = document.getElementById("cust_list");
  var tableRef = document.getElementById("acctTable");
  url='https://shopifyorder.herokuapp.com/accounts';
  $.ajax({
    url: url,
    type: 'GET',
    dataType: "json",
    success: function (data) {
      var df=data["names"];
      for (var i=0; i<df.length; i++){
        var name=df[i];
        select.options[select.options.length] = new Option(name, name);
        var link = document.createElement("a");
        link.setAttribute("href", "http://www.microsoft.com")
        link.className = "someCSSclass";
        var newRow   = tableRef.insertRow(tableRef.rows.length);
        var newCell  = newRow.insertCell(0);
        var newText  = document.createTextNode(name);
        link.appendChild(newText);
        newCell.appendChild(link);
      }
    },
    error: function(jqxhr, status, exception) {
        alert('Exception:', exception);
    }
  });
}

function checkPassword(){
  var pass=false;
  while (pass==false){
    var password="urbanfox2018";
    var ans=prompt("please enter your password","");
    if (password==ans){
      pass=true;
    }
  }
}

function onload(){
  checkPassword();
  getShops();
}
