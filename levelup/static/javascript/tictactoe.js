$(document).ready( function () {

    set_frame_resolution();

    $('#start-game').click(function(){
        enabled = true;
    });

    $('#pause-game').click(function(){
        enabled = false;
        stop_timer();
        save_game_state();
    });

    $('#load-game').click(function(){
        load_request();
    });

    addWebAppMessageListener();

    // Cell click handler
    $('.row>span').click(function() {
        if (!clicked){
            // if first click in the grid, start the timer
            start_timer();
            clicked = true;
        }
        if (enabled) {
            if ($(this).text().length == 0) {
                if (counter % 2 == 0) {
                    $(this).text('X');
                } else {
                    $(this).text('O');
                }
                board_dict[this.id] = $(this).text();
                var winner = check_board();
                if (winner == 'X') {
                    stop_timer();
                    send_score(calculate_final_score());
                    enabled = false;
                }
                counter++;
            }
        }
    });

});

var counter = 0, // counts the number of clicks in the grid (used to alternate Xs and Os)
    board_dict = {},
    enabled = true,
    start_time, // in milliseconds
    end_time, // in milliseconds
    total_time, // in seconds
    previous_time = 0,
    clicked = false;

function init_board(board){
    $('.wrapper span').each(function(){
        $(this).text(board[this.id]);
        board_dict[this.id] = board[this.id];
    });
}

function check_board() {
    for ( var i=0; i<3; i++ ) {
        var row = [board_dict[int_to_string_value(3*i)],
                    board_dict[int_to_string_value(3*i+1)],
                    board_dict[int_to_string_value(3*i+2)]];
        if ( check_triplet(row, 0) ) {
            color_winner_cells_triplet([3*i,3*i+1,3*i+2]);
            return row[0];
        }

        var column = [board_dict[int_to_string_value(i)],
                        board_dict[int_to_string_value(i+3)],
                        board_dict[int_to_string_value(i+6)]];
        if ( check_triplet(column, 0) ) {
            color_winner_cells_triplet([i,i+3,i+6]);
            return row[0];
        }
    }

    var diagonal = [board_dict[int_to_string_value(0)],
                    board_dict[int_to_string_value(4)],
                    board_dict[int_to_string_value(8)]];
    if ( check_triplet(diagonal, 0) ) {
        color_winner_cells_triplet([0,4,8]);
        return diagonal[0];
    }

    diagonal = [board_dict[int_to_string_value(2)],
                board_dict[int_to_string_value(4)],
                board_dict[int_to_string_value(6)]];
    if ( check_triplet(diagonal, 0) ) {
        color_winner_cells_triplet([2,4,6]);
        return diagonal[0];
    }
    return false;
}

function check_triplet(row, index) {
    if ( row[index] == row[index+1] && row[index] == 'X' || row[index] == row[index+1] && row[index] == 'O') {
        if ( index == 1 ) {
            return true;
        }
        return check_triplet(row, index + 1);
    }
    return false;
}

function color_winner_cells_triplet(indexes) {
    for (var i = 0; i < indexes.length; i++) {
        $('.wrapper').find('span#' + int_to_string_value(indexes[i])).css("background-color", "green");
    }
}

function int_to_string_value(int_value){
    if (int_value == 0) {
        return 'first';
    } else if (int_value == 1) {
        return 'second';
    } else if (int_value == 2) {
        return 'third';
    } else if (int_value == 3) {
        return 'fourth';
    } else if (int_value == 4) {
        return 'fifth';
    } else if (int_value == 5) {
        return 'sixth'
    } else if (int_value == 6) {
        return 'seventh';
    } else if (int_value == 7) {
        return 'eight';
    } else if (int_value == 8) {
        return 'ninth';
    }
}

function start_timer() {
    start_time = new Date().getTime();
}

function stop_timer() {
    end_time = new Date().getTime();
    calculate_total_time();
}

function calculate_total_time() {
    total_time = ((end_time - start_time) / 1000) % 60 + previous_time;
}

function calculate_final_score(){
    // The final score is calculated based on the time and the number of moves.
    // It is calculated as follows: moves*time (1 < final_score < 100)
    // The points are distributed like this:
    // - Moves :
    //      0 < moves < 3: 10 points
    //      4 moves      : 5  points
    //      moves > 5    : 1  point
    // - Time (every 3 seconds points are decreased by 1):
    //      3s           : 10 points
    //      3 < time <= 6: 9 points
    //      ...
    //      30s          : 1  point
    // Maximum score = 10 points (3 moves) * 10 points (<3s) = 100
    // Mininum score = 1 point (5 moves) * 1 point (>30s) = 1
    var moves_score = calculate_moves_score();
    var time_score = calculate_time_score();
    return moves_score * time_score;
}

function calculate_moves_score(){
    var moves_score = 0;
    var moves_counter = counter/2;
    if (moves_counter >= 0 && moves_counter <= 3){
        moves_score = 10;
    } else if (moves_counter == 4){
        moves_score = 5;
    } else {
        moves_score = 1;
    }
    return moves_score;
}

function calculate_time_score(){
    var x = total_time / 3;
    x = parseInt(x.toString()); // keep only the decimal part, without approximation
    return 10 - x;
}

function addWebAppMessageListener(){
    window.addEventListener("message", function(evt) {
        if(evt.data.messageType === "LOAD") {
            board_dict = evt.data.gameState.board;
            previous_time = evt.data.gameState.time;
            counter = evt.data.gameState.moves_count;
            init_board(board_dict);
        } else if (evt.data.messageType === "ERROR") {
            alert(evt.data.info);
        }
    });
}

function load_request () {
    var msg = {
        "message_type": "LOAD_REQUEST"
    };
    window.parent.postMessage(msg, "*");
}

function save_game_state(){
    $('.wrapper span').each(function(){
        board_dict[this.id] = $(this).text();
    });
    var msg = {
        "messageType": "SAVE",
        "gameState": {
            "board": board_dict,
            "time": parseFloat(total_time),
            "moves_count": counter
        }
    };
    window.parent.postMessage(msg, "*");
}

function send_score (score){
    var msg = {
        "messageType": "SCORE",
        "score": score
    };
    window.parent.postMessage(msg, "*");
}

function set_frame_resolution(){
    // Request the service to set the resolution of the iframe
    var message =  {
        messageType: "SETTING",
        options: {
            "width": 700, //Integer
            "height": 400 //Integer
        }
    };
    window.parent.postMessage(message, "*");
}