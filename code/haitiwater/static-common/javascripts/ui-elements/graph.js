// Call refresh when loading so that the first graph in the list is displayed
refresh();

// Request the JSON from server and update the graph
function refresh(){
    switch (document.getElementById('graphTitle').value){
        case 'consumerSexPie':
            consumerSexPie();
            break;
        default:
            console.log("Undefined graph type: " + document.getElementById('graphTitle').value)
    }
}

/**
 * Get the colors that will be used in the graphs.
 * You can put more colors, or less (but in the latter, you will have an ugly graph)
 * @returns {string[]}
 */
function colorThemes(){
    return [
        '#98C1D9',
        '#EE6C4D',
        '#293241'
    ]
}

function consumerSexPie(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/graph/?type=consumer_sex_pie";
    $.getJSON(dataURL, function(jsonfile) {
        var labels = jsonfile.jsonarray.map(function(e) {
           return e.label;
        });
        var data = jsonfile.jsonarray.map(function(e) {
           return e.data;
        });
        var ctx = canvas.getContext('2d');
        var config = {
           type: 'doughnut',
           data: {
              labels: labels,
              datasets: [{
                  data: data,
                  backgroundColor: colorThemes(),
              }]
           },
           options: {
               tooltips: {
                    callbacks: {
                        label: function(tooltipItem, data) {
                            let name = labels[tooltipItem.index];
                            let dataset = data.datasets[tooltipItem.datasetIndex];
                            let total = dataset.data.reduce(function(previousValue, currentValue, currentIndex, array) {
                                return previousValue + currentValue;
                            });
                            let currentValue = dataset.data[tooltipItem.index];
                            let percentage = Math.floor(((currentValue/total) * 100)+0.5);

                            return currentValue + ' ' + name + ' (' + percentage + '%)';
                        }
                    }
               }
           }
        };
        var chart = new Chart(ctx, config);
    }).done( function() {
    }).fail( function() {
        console.log("Failed graph request")
    }).always( function() {
    });
}