function butClick(){
  url='https://shopifyorder.herokuapp.com/orders';
  var e = document.getElementById("cust_list");
  var shopName = e.options[e.selectedIndex].value;
  if (shopName==""){
    alert("Please select an account.");
  }else{
    document.getElementById("loading").style.display="block";
    var finalUrl=url+'?name='+shopName;
    $.ajax({
      url: finalUrl,
      type: 'GET',
      success: function (data) {
        alert("success");
        csv = 'data:text/csv;charset=utf-8,' + encodeURI(data);
        link = document.createElement('a');
        link.setAttribute('href', csv);
        link.setAttribute('download', "download.csv");
        link.click();
        document.getElementById("loading").style.display="none";
      },
      error: function(jqxhr, status, exception) {
          alert('Exception:', exception);
          document.getElementById("loading").style.display="none";
      }
    });
  }
}

function validateAcctFields(){
  var fields = document.getElementsByClassName("fields");
  var i;
  var check = true;
  for (i = 0; i < fields.length; i++) {
      var tem= fields[i].value;
      if (fields[i].value==""){
        fields[i].style.backgroundColor = "red";
        check=false;
      }
  }

  if (!check){
    alert("Please fill in all fields in red to create an account.");
    fields[0].focus();
  }

  return check;
}

function createAccount(e){
  document.getElementById("loading").style.display="block";
  if (validateAcctFields()){
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
      success: function (data) {
        alert(data);
        location.reload();
      },
      error: function(data){
        alert(data);
      }
    });
  }
  document.getElementById("loading").style.display="none";
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
        link.setAttribute("href", "account.html")
        link.className = "someCSSclass";
        var newRow   = tableRef.insertRow(tableRef.rows.length);
        var newCell  = newRow.insertCell(0);
        var newText  = document.createTextNode(name);
        link.appendChild(newText);
        newCell.appendChild(link);
        document.getElementById("loading").style.display="none";
      }
    },
    error: function(jqxhr, status, exception) {
        alert('Exception:', exception);
        document.getElementById("loading").style.display="none";
    }
  });
}

function checkPassword(){
  var x = document.cookie;
  if (x!="logged in"){
    var pass=false;
    while (pass==false){
      var password="urbanfox2018";
      var ans=prompt("please enter your password","");
      if (password==ans){
        pass=true;
        document.cookie = "logged in";
      }
    }
  }
}

function onload(){
  checkPassword();
  getShops();
}
