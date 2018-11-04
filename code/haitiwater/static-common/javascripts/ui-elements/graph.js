jsonfile = null;
dataURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '') + "/api/graph/?type=json";

//ToDo next iteration, use this one
$.getJSON(dataURL, function() {
    console.log("1")
}).done( function() {
    console.log("2")
}).fail( function(e) {
    console.log(e)
}).always( function() {
    console.log("4")
});

//ToDo move up to allow failure
$.getJSON(dataURL, function(jsonfile) {
    var labels = jsonfile.jsonarray.map(function(e) {
       return e.name;
    });
    var data = jsonfile.jsonarray.map(function(e) {
       return e.age;
    });

    var ctx = canvas.getContext('2d');
    var config = {
       type: 'line',
       data: {
          labels: labels,
          datasets: [{
             label: 'Graph Line',
             data: data,
             backgroundColor: 'rgba(0, 119, 204, 0.3)'
          }]
       }
    };

    var chart = new Chart(ctx, config);
});