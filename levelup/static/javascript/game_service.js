var SETTING_MESSAGE = 'SETTING';
var LOAD_REQUEST_MESSAGE = 'LOAD_REQUEST';
var LOAD_MESSAGE = 'LOAD';
var ERROR_MESSAGE = 'ERROR';
var SCORE_MESSAGE = 'SCORE';
var SAVE_MESSAGE = 'SAVE';

var ACCEPTED_MESSAGES = [SETTING_MESSAGE, LOAD_REQUEST_MESSAGE, LOAD_MESSAGE, ERROR_MESSAGE, SCORE_MESSAGE, SAVE_MESSAGE]

$(document).ready(function() {

    ajaxSetup();

    $(window).on('message', function(evt) {

        var data = evt.originalEvent.data;
        var message = data.messageType;

        console.log(message);

        if ($.inArray(message, ACCEPTED_MESSAGES) != -1){
            switch (message){
                case LOAD_REQUEST_MESSAGE:
                    loadPreviousGame();
                    break;
                case SAVE_MESSAGE:
                    saveGameState(data);
                    break;
                case SCORE_MESSAGE:
                    saveGameScore(data);
                    break;
                case SETTING_MESSAGE:
                    resizeGameFrame(data);
                    break;
            }
        }
    });

    $('#game_resume').click(function () {
        loadPreviousGame();
    });

    $('#game_new').click(function () {
        startNewGame();
    });
});

function resizeGameFrame( data ){
    var game_frame = document.getElementById("game_frame");
    game_frame.width = data.options.width;
    game_frame.height = data.options.height;

    $('#game_resume').show();
    $('#game_new').show();
}

function loadPreviousGame(){
    var game_state = $("#game_state").val();
    var message = null;

    /*
    CASE 0: the user loads the page and there is a previous saved game -> load the game state (var game_state) with the
            data saved in the database
    CASE 1: the user loads the page, plays and then saves a game. Then he/she does not reload the page and resume the game
            -> load the saved game state (var game_state_global) from the current session
     */
    if (game_state_global){
        // the user has a saved game which was saved during this session
        game_state_global = formatGameState(game_state_global);
        console.log('game_state_global', game_state_global)
        message = {
            messageType: "LOAD",
            gameState: game_state_global
        };
    } else if (game_state){
        // there is a previously saved game in the database (the user just arrived in the page)
        game_state = formatGameState(game_state);
        console.log('game_state', game_state)
        // game_state = JSON.parse(game_state);
        message = {
            messageType: "LOAD",
            gameState: game_state
        };
    } else {
        // there is no previously saved game
        message =  {
            messageType: "ERROR",
            info: "No previous saved game found."
        };
    }

    var game_frame = document.getElementById("game_frame").contentWindow;
    game_frame.postMessage(message, '*');

    // Remove the blurry layer on top of the iframe and hide the resume button
    $("iframe").css("filter","none");
    $('#game_resume').hide();
}

var game_state_global = null;
function saveGameState( data ){
    var game_state = data.gameState;
    game_state = JSON.stringify(game_state);
    game_state_global = game_state;

    console.log('save game_state_global', game_state_global)

    var game_state_url = $("#game_state_url").val();

    $.ajax({
        url: game_state_url,
        type: 'POST',
        data: {
            'game_state': game_state
        },
        success: function( data ){
            $("iframe").css("filter","blur(5px)");
            $('#game_resume').show();
        },
        fail: function( jqXHR, textStatus ) {
            console.log("Request failed: " + textStatus );
        }
    });
}

function saveGameScore(data) {
    var game_score_url = $("#game_score_url").val();
    $.ajax({
        url: game_score_url,
        type: 'POST',
        data: {
            'game_score': data.score
        },
        success: function( data ){
            location.reload();
        },
        fail: function( jqXHR, textStatus ) {
            console.log("Request failed: " + textStatus );
        }
    });
}

function startNewGame(){
    if (game_state_global){
        location.reload();
    } else {
        $("iframe").css("filter","none");
        $('#game_resume').hide();
        $('#game_new').hide();
    }
}

function formatGameState(game_state){
    if (game_state.constructor == String) {
        game_state = JSON.parse(game_state);
    }
    if (!('score' in game_state)){
        game_state.points = 0;
    }
    if (!('playerItems' in game_state)){
        game_state.playerItems = [];
    }
    return game_state
}

function ajaxSetup(){
    var csrftoken = Cookies.get('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function csrfSafeMethod( method ) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}