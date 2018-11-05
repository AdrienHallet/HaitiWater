// Call refresh when loading so that the first graph in the list is displayed
refresh();

// Request the JSON from server and update the graph
function refresh(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/graph/?type=" + document.getElementById("graphTitle").value;
    console.log(dataURL)
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
    }).done( function() {
        console.log("Finished graph request")
    }).fail( function() {
        console.log("Failed graph request")
    }).always( function() {
        console.log("Closing graph request")
    });
}