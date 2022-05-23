google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(onChartsLoad);

const select = document.getElementById("tickers_select");
const current_ticker = select.selectedOptions[0].value;
let ws = new WebSocket(`ws://${window.location.host}/realtime_data/${current_ticker}`);
const chart_options = {
    hAxis: {
        title: 'Time'
    },
    vAxis: {
        title: 'Value'
    },
    curveType: 'function'
};

let data_table;
let chart;

async function onChartsLoad(){
    chart = new google.visualization.LineChart(document.getElementById('chart_div'));

    const current_ticker = select.selectedOptions[0].value;
    data_table = await prepare_data(current_ticker);
    chart.draw(data_table, chart_options);

    ws.addEventListener(
        'message',
        on_message
    );

    select.addEventListener(
        'change',
        async function (event) {
            const current_ticker = select.selectedOptions[0].value;
            data_table = await prepare_data(current_ticker);
            chart.draw(data_table, chart_options);
            ws.close();
            ws = new WebSocket(`ws://${window.location.host}/realtime_data/${current_ticker}`);
            ws.addEventListener(
                'message',
                on_message
            );
        }
    );
}

function on_message(event) {
    const ticker_data = JSON.parse(event.data);
    ticker_data[0] = new Date(Date.parse(ticker_data[0]));
    data_table.addRow(ticker_data);
    chart.draw(data_table, chart_options);
}

async function prepare_data(current_ticker){
    const data = await(await fetch(`http://${window.location.host}/ticker_entries/${current_ticker}`)).json();
    data.forEach(
        item => {
            item[0] = new Date(Date.parse(item[0]));
        }
    );
    data_table = new google.visualization.DataTable();
    data_table.addColumn('date', 'time');
    data_table.addColumn('number', 'value');
    data_table.addRows(data);
    return data_table;
}