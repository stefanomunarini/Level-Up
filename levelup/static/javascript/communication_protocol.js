function save_game_state (score) {
    var msg = {
        "messageType": "SAVE",
        "gameState": {
            "board": board,
            "score": parseFloat(score)
        }
    };
    window.parent.postMessage(msg, "*");
}

function save_score (score) {
    var msg = {
        "message_type": "SCORE",
        "score": parseFloat(score)
    }
    window.parent.postMessage(msg, "*");
}

function load_request () {
    var msg = {
        "message_type": "LOAD_REQUEST"
    }
    window.parent.postMessage(msg, "*");
}