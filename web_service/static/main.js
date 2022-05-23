google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(onChartsLoad);


async function onChartsLoad(){
    const data_table = new google.visualization.DataTable();
    data_table.addColumn('date', 'time');
    data_table.addColumn('number', 'value');
    const chart_options = {
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: 'Value'
        }
    };

    const select = document.getElementById("tickers_select");
    currentTicker = select.selectedOptions[0].value;

    let data = await(await fetch(`http://${window.location.host}/ticker_entries/${currentTicker}`)).json();
    console.log(data);
    data.forEach(
        item => {
            item[0] = new Date(Date.parse(item[0]));
        }
    );

    data_table.addRows(data);
    draw(data_table, chart_options);
    const ws = new WebSocket(`ws://${window.location.host}/realtime_data/${currentTicker}`);
    ws.addEventListener(
        'message',
        function (event) {
            console.log('Message from server ', event.data);
        }
    );
}

function draw(data_table, chart_options) {
      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
      chart.draw(data_table, chart_options);
}


//const ws = new WebSocket(`ws://${window.location.host}/realtime_data`);
