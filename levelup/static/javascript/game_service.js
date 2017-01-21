SETTING_MESSAGE = 'SETTING';
LOAD_REQUEST_MESSAGE = 'LOAD_REQUEST';
LOAD_MESSAGE = 'LOAD';
ERROR_MESSAGE = 'ERROR';
SCORE_MESSAGE = 'SCORE';
SAVE_MESSAGE = 'SAVE';

ACCEPTED_MESSAGES = [SETTING_MESSAGE, LOAD_REQUEST_MESSAGE, LOAD_MESSAGE, ERROR_MESSAGE, SCORE_MESSAGE, SAVE_MESSAGE]

$(document).ready(function() {
    console.log('ciao');
    $(window).on('message', function(evt) {
        data = evt.originalEvent.data
        message = data.messageType
        console.log(message)
        if ($.inArray(message, ACCEPTED_MESSAGES) != -1){
            console.log('yes')
            switch (message){
                case SETTING_MESSAGE:
                    $('game_frame').width = data.options.width;
                    $('game_frame').height = data.options.height;
                default:
                    console.log('nothing here')
            }

        }
    });
});
