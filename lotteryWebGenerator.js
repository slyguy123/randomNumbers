function submitForm(e) {
  var t = "";
  var n = true;
  var r = true;
  var a = false;
  e.action;

  for (var x = 1; x < document.getElementsByClassName("widget-line").length + 1; x++) {
    var u = true;

    for (var y = 1; y < m + b + 1; y++) {
      var o = document.getElementById("jn_" + x + "_" + y).value;

      if ("" != o && isNumeric(o, y)) {
        u = false;
      }

      if (!isNumeric(o, y)) {
        r = false;
      }

      if (duplicates(x)) {
        a = true;
      }

      if ("" != o) {
        n = false;
      }
    }

    if (u) {
      t = x;
    }
  }

  if ("" != t && r && !a) {
    var l = {};

    l.LotteryID = e.BrandID.value;
    l.Type = 1;
    l.Lines = [];

    for (var i = 1; i <= t; i++) {
      var c = {
        MainNumbers: [],
        BonusNumbers: []
      };

      for (var j = 1; j <= m; j++) {
        c.MainNumbers.push(document.getElementById("jn_" + i.toString() + "_" + j.toString()).value);
      }

      for (var j = m + 1; j <= m + b; j++) {
        c.BonusNumbers.push(document.getElementById("jn_" + i.toString() + "_" + j.toString()).value);
      }

      l.Lines.push(c);
    }

    var d = JSON.stringify(l);
    var s = new XMLHttpRequest();

    s.open("POST", "https://api.jackpot.com/api/ext/play-combinations", false);

    s.onreadystatechange = function() {
      if (4 == this.readyState && 200 == this.status) {
        var t = "";

        try {
          var n = JSON.parse(this.responseText);
          t = n.Token;
        } catch (e) {
          t = "";
        }

        e.ticket.value = t;
      }
    };

    s.send(d);
    return true;
  }

  if (!n) {
    if (a) {
      alert("You have duplicate numbers! Please review your selections.");
      return false;
    } else {
      alert("Please complete your line with valid numbers.");
      return false;
    }
  }

  return true;
}

function isNumeric(e, t) {
  var n = "" == e || (!isNaN(parseFloat(e)) && isFinite(e));
  var i = true;

  if ("" != e) {
    if (t <= m && n) {
      i = e >= 1 && e <= mp;
    } else if (t > m && t <= m + b && n) {
      i = e >= 1 && e <= bp;
    }
  }

  return n && i;
}
// Setup cool count down cycle 
function quickPick(e) {
  for (var i = 1; i < m + 1; i++) {
    if (!document.getElementById("jn_" + e + "_" + i).SpinTimer) {
      document.getElementById("jn_" + e + "_" + i).SpinTimer = setInterval("document.getElementById('jn_" + e + "_" + i + "').value = Math.floor((Math.random()*" + mp + ")+1)", 40);
    }
  }

  if (b > 0) {
    for (var i = m + 1; i < m + b + 1; i++) {
      if (!document.getElementById("jn_" + e + "_" + i).SpinTimer) {
        document.getElementById("jn_" + e + "_" + i).SpinTimer = setInterval("document.getElementById('jn_" + e + "_" + i + "').value = Math.floor((Math.random()*" + bp + ")+1)", 40);
      }
    }
  }

  setTimeout(function() {
    for (var i = 1; i < m + b + 1; i++) {
      clearInterval(document.getElementById("jn_" + e + "_" + i).SpinTimer);
      document.getElementById("jn_" + e + "_" + i).SpinTimer = false;

      var t = checkDuplicates(i, e);

      while (t) {
        t = checkDuplicates(i, e);
      }
    }
  }, 300);
}

function checkDuplicates(e, t) {
  if (e <= m) {
    for (var n = 1; n < m + 1; n++) {
      var i = document.getElementById("jn_" + t + "_" + e);
      var r = document.getElementById("jn_" + t + "_" + n);

      if (n != e && i.value == r.value) {
        i.value = Math.floor(Math.random() * mp + 1);
        return true;
      }
    }
  }

  if (b > 0 && e > m) {
    for (var n = m + 1; n < m + b + 1; n++) {
      var i = document.getElementById("jn_" + t + "_" + e);
      var r = document.getElementById("jn_" + t + "_" + n);

      if (n != e && i.value == r.value) {
        i.value = Math.floor(Math.random() * bp + 1);
        return true;
      }
    }
  }

  return false;
}

function duplicates(e) {
  for (var t = 1; t < m + 1; t++) {
    for (var n = document.getElementById("jn_" + e + "_" + t), i = t + 1; i < m + 1; i++) {
      var r = document.getElementById("jn_" + e + "_" + i);

      if (t != i && n.value == r.value && "" != n.value) {
        return true;
      }
    }
  }

  if (b > 0) {
    for (var t = m + 1; t < m + b + 1; t++) {
      for (var n = document.getElementById("jn_" + e + "_" + t), i = t + 1; i < m + b + 1; i++) {
        var r = document.getElementById("jn_" + e + "_" + i);

        if (t != i && n.value == r.value && "" != n.value) {
          return true;
        }
      }
    }
  }

  return false;
}

function clearLine(e) {
  for (var i = 1; i < m + b + 1; i++) {
    document.getElementById("jn_" + e + "_" + i).value = "";
  }
}
