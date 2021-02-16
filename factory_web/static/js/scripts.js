function getTimeRemaining(end_time) {
    var t =  Date.parse(new Date()) - Date.parse(end_time);
    var seconds = Math.floor((t / 1000) % 60);
    var minutes = Math.floor((t / 1000 / 60) % 60);
    var hours = Math.floor(t / (1000 * 60 * 60));
    return {
        'total': t,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    };
}

function initializeClock(id, end_time) {
    var clock = document.getElementById(id);
    var hoursSpan = clock.querySelector('.hours');
    var minutesSpan = clock.querySelector('.minutes');
    var secondsSpan = clock.querySelector('.seconds');

    function updateClock() {
        var t = getTimeRemaining(end_time);

        hoursSpan.innerHTML = t.hours
        minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
        secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

    document.getElementById("stop").addEventListener('click', function() {
        clearInterval(time_interval);
    })
    }

    updateClock();
    var time_interval = setInterval(updateClock, 1000);
}


var options = {month: 'long', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'};
//var deadline = new Date().toLocaleDateString('en-US', options);


$(document).ready(function(){

    $.ajax({
        url: '',
        type: 'get',
        success: function(response) {
            if (response.seconds) {
                initializeClock('countdown', response.seconds);
            } else {}
        }
    });

    $('#start').click(function(){
       $.ajax({
           url: '',
           type: 'get',
           data: {
               button_text: new Date().toLocaleDateString('en-US', options)
           },
           success: function(response) {
               initializeClock('countdown', response.seconds);
           }
       });
    });

    $('#stop').click(function(){
       $.ajax({
           url: '',
           type: 'get',
           data: {
               button_text: 'stop'
           },
           success: function(response) {
           }
       });
    });

})
