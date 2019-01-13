const GALLONS_PER_CUBIC = 264.17205235815;

$(document).ready(function() {
    // Keep the same graph selected across refresh
    if (localStorage.graphTitle) {
        $('#graphTitle').val(localStorage.graphTitle);
        refresh();
    }
});

// Update the graph selection value
$('#graphTitle').on('change', function(){
    let currentVal = $(this).val();
    localStorage.setItem('graphTitle', currentVal );
});

// Call refresh when loading so that the first graph in the list is displayed
refresh();

// Request the JSON from server and update the graph
function refresh() {
    // First clean old graph
    let graphDiv = $('#graph-div');
    graphDiv.empty();
    graphDiv.append('<canvas id="graph-canvas"></canvas>');
    // Request new draw
    switch (document.getElementById('graphTitle').value) {
        case 'consumerGenderPie':
            consumerGenderPie();
            break;
        case 'averageMonthlyVolumePerZone':
            monthlyVolumePerZone();
            break;
        case 'none':
            break; // empty case
        default: // error case
            console.log("Undefined graph type: " + document.getElementById('graphTitle').value)
    }
}

/**
 * Get the colors that will be used in the graphs.
 * You can put more colors, or less (but in the latter, you will have an ugly graph)
 * @returns {string[]}
 */
function colorThemes() {
    return [
        '#98C1D9',
        '#EE6C4D',
        '#293241'
    ]
}

function consumerGenderPie() {
    let baseURL = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
    let dataURL = baseURL + "/api/graph/?type=consumer_gender_pie";
    $.getJSON(dataURL, function (jsonfile) {
        var labels = jsonfile.jsonarray.map(function (e) {
            return e.label;
        });
        var data = jsonfile.jsonarray.map(function (e) {
            return e.data;
        });
        var ctx = document.getElementById('graph-canvas').getContext('2d');
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
                        label: function (tooltipItem, data) {
                            let name = labels[tooltipItem.index];
                            let dataset = data.datasets[tooltipItem.datasetIndex];
                            let total = dataset.data.reduce(function (previousValue, currentValue, currentIndex, array) {
                                return previousValue + currentValue;
                            });
                            let currentValue = dataset.data[tooltipItem.index];
                            let percentage = Math.floor(((currentValue / total) * 100) + 0.5);

                            return currentValue + ' ' + name + ' (' + percentage + '%)';
                        }
                    }
                }
            }
        };
        var chart = new Chart(ctx, config);
    }).done(function () {
    }).fail(function () {
        console.log("Failed graph request")
    }).always(function () {
    });
}

function monthlyVolumePerZone() {
    let baseURL = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
    let dataURL = baseURL + "/api/graph/?type=average_monthly_volume_per_zone";
    $.getJSON(dataURL, function (jsonfile) {
        var labels = jsonfile.jsonarray[0].label;
        var data = jsonfile.jsonarray[0].data;
        var gallonData = new Array(data.length);
        for (var i = 0; i < data.length; i++) {
            gallonData[i] = data[i] * GALLONS_PER_CUBIC;
        }
        var ctx = document.getElementById('graph-canvas').getContext('2d');
        var config = {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: "Mètres cubes",
                    data: data,
                    yAxisID: "y-axis-0",
                    backgroundColor: colorThemes()[0],
                }, {
                    label: "Gallons",
                    data: gallonData,
                    yAxisID: "y-axis-1",
                    backgroundColor: colorThemes()[1]
                }]
            },
            options: {
                tooltips: {
                    mode: 'label'
                },
                responsive: true,
                scales: {
                    yAxes: [{
                        position: "left",
                        id: "y-axis-0",
                        scaleLabel: {
                            display: true,
                            labelString: 'Mètres cubes'
                        },
                        ticks: {
                            beginAtZero: true
                        }
                    }, {
                        position: "right",
                        id: "y-axis-1",
                        scaleLabel: {
                            display: true,
                            labelString: 'Gallons'
                        },
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                legend: {
                    onClick: function(event, legendItem) {
                        //get the index of the clicked legend
                        let index = legendItem.datasetIndex;
                        //toggle chosen dataset's visibility
                        chart.data.datasets[index].hidden =
                            !chart.data.datasets[index].hidden;
                        //toggle the related labels' visibility
                        chart.options.scales.yAxes[index].display =
                            !chart.options.scales.yAxes[index].display;
                        chart.update();
                    }
                }
            }
        };
        var chart = new Chart(ctx, config);
    }).done(function () {
    }).fail(function () {
        console.log("Failed graph request")
    }).always(function () {
    });
}