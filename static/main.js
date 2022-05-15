const ws = new WebSocket(`ws://${window.location.host}/realtime_data`);
ws.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
});