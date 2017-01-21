var SETTING_MESSAGE = 'SETTING';
var LOAD_REQUEST_MESSAGE = 'LOAD_REQUEST';
var LOAD_MESSAGE = 'LOAD';
var ERROR_MESSAGE = 'ERROR';
var SCORE_MESSAGE = 'SCORE';
var SAVE_MESSAGE = 'SAVE';

var ACCEPTED_MESSAGES = [SETTING_MESSAGE, LOAD_REQUEST_MESSAGE, LOAD_MESSAGE, ERROR_MESSAGE, SCORE_MESSAGE, SAVE_MESSAGE]

$(document).ready(function() {

    $(window).on('message', function(evt) {
        data = evt.originalEvent.data
        message = data.messageType
        if ($.inArray(message, ACCEPTED_MESSAGES) != -1){
            switch (message){
                case SETTING_MESSAGE:
                    var game_frame = document.getElementById("game_frame");
                    game_frame.width = data.options.width;
                    game_frame.height = data.options.height;
                case LOAD_REQUEST_MESSAGE:
                    var game_state = JSON.parse($("#game_state").val());
                    // console.log('game_state', game_state)
                    var message = {
                        messageType: "LOAD",
                        gameState: game_state
                    };
                    var game_frame = document.getElementById("game_frame").contentWindow;
                    game_frame.postMessage(message, '*')
                default:
                    console.log('nothing here')
            }

        }
    });
});
