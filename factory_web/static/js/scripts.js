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

function buttons_disable(){
    $('#stop').attr('disabled', 'disabled');
    $('#plan').attr('disabled', 'disabled');
    $('#setup').attr('disabled', 'disabled');
    $('#auto_serv').attr('disabled', 'disabled');
    $('#breaking').attr('disabled', 'disabled');
    $('#task').attr('disabled', 'disabled');
    $('#material').attr('disabled', 'disabled');
    $('#ppr').attr('disabled', 'disabled');
    $('#model').attr('disabled', 'disabled')
}

function buttons_enable(){
    $('#stop').removeAttr('disabled');
    $('#plan').removeAttr('disabled');
    $('#setup').removeAttr('disabled');
    $('#auto_serv').removeAttr('disabled');
    $('#breaking').removeAttr('disabled');
    $('#task').removeAttr('disabled');
    $('#material').removeAttr('disabled');
    $('#ppr').removeAttr('disabled');
    $('#model').removeAttr('disabled')
}

buttons_disable()

$(document).ready(function(){

    let csrf = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        url: '',
        type: 'get',
        success: function(response) {
            if (response.seconds) {
                initializeClock('countdown', response.seconds);
                $('#start').attr('disabled', 'disabled')
                buttons_enable()
            }
            if (response.seconds1) {
                initializeClock('countdown1', response.seconds1);
                buttons_disable()
                $(response.button_choice).removeAttr('disabled');
            }
        }
    });

    $('#start').click(function(){
        $('#this').attr('disabled', 'disabled')
        buttons_enable()
        $.ajax({
            url: '',
            type: 'get',
            data: {
                button_text: new Date().toLocaleDateString('en-US', options)
            }
        });
    });

    $('#start').click(function(){
        $('#this').attr('disabled', 'disabled')
        buttons_enable()
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'start',
                csrfmiddlewaretoken: csrf
            }
        });
    });

    $('#stop').click(function(){
        $('#start').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'get',
            data: {
                button_text: 'stop'
            }
        });
    });

    $('#stop').click(function(){
        $('#start').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'stop',
                csrfmiddlewaretoken: csrf
            }
        });
    });

    $('#plan').click(function(){
        buttons_disable();
        $('#plan').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'get',
            data: {
                new_button_text: new Date().toLocaleDateString('en-US', options)
            }
        });
    });

    $('#plan').click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'start plan counter',
                action1: 'stop plan counter',
                csrfmiddlewaretoken: csrf
            }
        });
    });

    $('#setup').click(function(){
        buttons_disable();
        $('#setup').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'get',
            data: {
                new_button_text: new Date().toLocaleDateString('en-US', options)
            }
        });
    });

    $('#setup').click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'start setup counter',
                action1: 'stop setup counter',
                csrfmiddlewaretoken: csrf
            }
        });
    });

    $('#auto_serv').click(function(){
        buttons_disable();
        $('#auto_serv').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'get',
            data: {
                new_button_text: new Date().toLocaleDateString('en-US', options)
            }
        });
    });

    $('#auto_serv').click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'start auto_serv counter',
                action1: 'stop auto_serv counter',
                csrfmiddlewaretoken: csrf
            }
        });
    });

    $('#ppr').click(function(){
        buttons_disable();
        $('#ppr').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'get',
            data: {
                new_button_text: new Date().toLocaleDateString('en-US', options)
            }
        });
    });

    $('#ppr').click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'start ppr counter',
                action1: 'stop ppr counter',
                csrfmiddlewaretoken: csrf
            }
        });
    });

    $('#breaking').click(function(){
        buttons_disable();
        $('#breaking').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'get',
            data: {
                new_button_text: new Date().toLocaleDateString('en-US', options)
            }
        });
    });

    $('#breaking').click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'start breaking counter',
                action1: 'stop breaking counter',
                csrfmiddlewaretoken: csrf
            }
        });
    });

    $('#material').click(function(){
        buttons_disable();
        $('#material').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'get',
            data: {
                new_button_text: new Date().toLocaleDateString('en-US', options)
            }
        });
    });

    $('#material').click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'start material counter',
                action1: 'stop material counter',
                csrfmiddlewaretoken: csrf
            }
        });
    });

    $('#task').click(function(){
        buttons_disable();
        $('#task').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'get',
            data: {
                new_button_text: new Date().toLocaleDateString('en-US', options)
            }
        });
    });

    $('#task').click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'start task counter',
                action1: 'stop task counter',
                csrfmiddlewaretoken: csrf
            }
        });
    });

    $('#model').click(function(){
        buttons_disable();
        $('#model').removeAttr('disabled');
        $.ajax({
            url: '',
            type: 'get',
            data: {
                new_button_text: new Date().toLocaleDateString('en-US', options)
            }
        });
    });

    $('#model').click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                action: 'start model counter',
                action1: 'stop model counter',
                csrfmiddlewaretoken: csrf
            }
        });
    });

})
