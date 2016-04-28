exampleSocket.onmessage = function(event) {
  var f = document.getElementById("table");
  var msg = JSON.parse(event.data);

  
  switch(msg.type) {
    
      document.getElementById("userlistbox").innerHTML = ul;
      break;
  }
  
  if (text.length) {
    f.write(text);
    document.getElementById("chatbox").contentWindow.scrollByPages(1);
  }
};
