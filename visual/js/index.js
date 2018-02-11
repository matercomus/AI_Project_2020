// Removes all cards that are not needed to play Schnapsen
function schnapsenDeck(){
    fullDeck = Deck();
    fullDeck.cards.forEach(function (card) {
        card.enableDragging()
        if(card.rank<10 && card.rank>1){
            card.unmount();
        }
    });
    return syncCardIndices(fullDeck)
}

// I feel disgusted with myself
function syncCardIndices(visualDeck){
    card_indices = [];

    card_indices.push(visualDeck.cards[26])
    card_indices.push(visualDeck.cards[35])
    card_indices.push(visualDeck.cards[38])
    card_indices.push(visualDeck.cards[37])
    card_indices.push(visualDeck.cards[36])

    card_indices.push(visualDeck.cards[39])
    card_indices.push(visualDeck.cards[48])
    card_indices.push(visualDeck.cards[51])
    card_indices.push(visualDeck.cards[50])
    card_indices.push(visualDeck.cards[49])

    card_indices.push(visualDeck.cards[13])
    card_indices.push(visualDeck.cards[22])
    card_indices.push(visualDeck.cards[25])
    card_indices.push(visualDeck.cards[24])
    card_indices.push(visualDeck.cards[23])

    card_indices.push(visualDeck.cards[0])
    card_indices.push(visualDeck.cards[9])
    card_indices.push(visualDeck.cards[12])
    card_indices.push(visualDeck.cards[11])
    card_indices.push(visualDeck.cards[10])

    visualDeck.backEndIndices = card_indices

    return visualDeck
}

function moveCard(card, xc, yc, rotc=0){
    card.animateTo({
        delay: 100,
        duration: 500,
        ease: 'quartOut',
        
        x: xc, //Math.random() * window.innerWidth - window.innerWidth / 2,
        y: yc, //Math.random() * window.innerHeight - window.innerHeight / 2
        rot: rotc
    });
}

// TODO order cards are stacked on top of each other
// revisit dealStock
// Check hardcoded card sizes and maybe do some hard coding of my own so that they don't overlap

function deal(visualDeck, currentState, previousState = null){
    height = window.innerHeight;
    width = window.innerWidth;

    changes_array = determineChanges(currentState, previousState);



}

function determineChanges(currentState, previousState = null){
    card_state_array = getCardStateArray(currentState);

    if(previousState){

        previous_state_array = getCardStateArray(previousState);
        changes_array = [];

        for(i=0; i<card_state_array.length; i++){

            if(card_state_array[i] != previous_state_array[i]){
                changes_array.push(card_state_array[i]);
            }

            else changes_array.push(null);
        }

    } else {
        changes_array = card_state_array;
    }

    return changes_array;
}

function dealStock(visualDeck, stock){
    height = window.innerHeight;
    width = window.innerWidth;
    stock.forEach(function(cardIndex, stockIndex){
        card = visualDeck.backEndIndices[cardIndex];

        if(stockIndex==0){
            card.setSide('front');
            moveCard(card, -3*width/8, -30, 0);
        } else {
            card.setSide('back');
            moveCard(card, -3*width/8, 0);
        }
    });
}

// TODO
function reorderArrayElement(array, srcIndex, targetIndex){
    if(srcIndex > targetIndex){

    }
}

function arrIsNull(arr){
    for(i=0; i<arr.length; i++){
        if (arr[i] != null){
            return false;
        }
    }
    return true;
}

function arrElemFreq(arr, elem){
    ct = 0;
    for(i=0; i<arr.length; i++){
        if(arr[i] == elem){
            ct++;
        }
    }
    return ct;
}

function orderCards(visualDeck, stock){

}

function arrangeCards(visualDeck, backEndState){
    p1placed = 0;
    p2placed = 0;
    p1wonCount=0;
    p2wonCount=0;

    x = null;
    y = null;

    height = window.innerHeight;
    width = window.innerWidth;

    card_states = getCardStateArray(backEndState);
    p1wonTotal = arrElemFreq(card_states, "P1W");
    p2wonTotal = arrElemFreq(card_states, "P2W");

    card_states.forEach(function(card_state, card_index){

        if(card_state == "P1H"){
            visualDeck.backEndIndices[card_index].setSide('front');

            x = width/3 + (p1placed/4)*(width/3) - width/2;
            y = height/4;

            p1placed++;

        } else if(card_state == "P2H"){
            visualDeck.backEndIndices[card_index].setSide('back');

            x = width/3 + (p2placed/4)*(width/3) - width/2;
            y = -height/4;

            p2placed++;

        } else if(card_state == "P1D"){
            visualDeck.backEndIndices[card_index].setSide('front');

            x = -width/24;
            y = 0;

            p1placed++;

        } else if(card_state == "P2D"){
            visualDeck.backEndIndices[card_index].setSide('front');

            x = width/24;
            y = 0;

            p2placed++;

        } else if(card_state == "P1W"){
            visualDeck.backEndIndices[card_index].setSide('front');

            x = width/4*(1 + (p1wonCount/(p1wonTotal+1)));
            y = height/2;

            p1wonCount++;

        } else if(card_state == "P2W"){
            visualDeck.backEndIndices[card_index].setSide('front');

            x = width/4*(1 + (p2wonCount/(p2wonTotal+1)));
            y = -height/2;

            p2wonCount++;
        }

        if(x!=null && y != null){
            moveCard(visualDeck.backEndIndices[card_index], x, y-10);
            x = null;
            y = null;
        }


    });
}

function initialCardSetup(visualDeck, backEndState){

    height = window.innerHeight;
    width = window.innerWidth;


    //STOCK
    if(!ordered){
        orderCards(visualDeck, backEndState.deck.stock);
        ordered = true;
    }

    dealStock(visualDeck, backEndState.deck.stock);

    // If we are at the start of a trick that is not the first.
    if(arrIsNull(backEndState.deck.trick) && !arrIsNull(backEndState.deck.previous_trick)){

        prev = backEndState.deck.previous_trick
        visualDeck.backEndIndices[prev[0]].setSide('front');
        moveCard(visualDeck.backEndIndices[prev[0]], -width/12, 0);

        visualDeck.backEndIndices[prev[1]].setSide('front');
        moveCard(visualDeck.backEndIndices[prev[1]], width/12, 0);


        setTimeout(function(){arrangeCards(visualDeck, backEndState);}, 1000);
    } else {
        arrangeCards(visualDeck, backEndState);
    }

    // backEndState.deck.card_state.forEach(function(card_state, card_index){

    //     if(card_state == "P1H"){

    //         visualDeck.backEndIndices[card_index].setSide('front');

    //         if(backEndState.deck.trick[0] != card_index){

    //             x = width/3 + (p1placed/4)*(width/3) - width/2;
    //             y = height/4

    //         } else {

    //             x = -width/24;
    //             y = 0;

    //         }
    //         p1placed++;

    //     }
    //     else if(card_state == "P2H"){

    //         if(backEndState.deck.trick[1] != card_index){

    //             visualDeck.backEndIndices[card_index].setSide('back');

    //             x = width/3 + (p2placed/4)*(width/3) - width/2;
    //             y = -height/4


    //         } else {

    //             visualDeck.backEndIndices[card_index].setSide('front');

    //             x = width/24;
    //             y = 0;

    //         }
    //         p2placed++;
    //     }
    //     if(x != null && y != null){
    //         moveCard(visualDeck.backEndIndices[card_index], x, y)
    //         x = null;
    //         y = null;
    //     }
    // });
}

function getCardStateArray(backEndState){
    card_state = backEndState.deck.card_state
    trick = backEndState.deck.trick

    for(i=0; i<2; i++){
        if(trick[i] != null){
            card_state[trick[i]] = "P" + parseInt(i+1) + "D"
        }
    }
    return card_state
}

var ordered = false;

// Get container
var $container = document.getElementById('container');

// Create Deck
var deck = schnapsenDeck();

// Add container to DOM
deck.mount($container);

// testState = {"p1_points": 0, "player1s_turn": true, "revoked": null, "p1_pending_points": 0, "p2_pending_points": 0, "deck": {"trump_suit": "H", "p1_perspective": ["U", "P1H", "U", "U", "P1H", "U", "U", "U", "U", "U", "U", "U", "S", "P1H", "U", "P1H", "U", "U", "U", "P1H"], "card_state": ["P2H", "P1H", "S", "S", "P1H", "S", "P2H", "P2H", "S", "P2H", "S", "P2H", "S", "P1H", "S", "P1H", "S", "S", "S", "P1H"], "p2_perspective": ["P2H", "U", "U", "U", "U", "U", "P2H", "P2H", "U", "P2H", "U", "P2H", "S", "U", "U", "U", "U", "U", "U", "U"], "trick": [null, null], "signature": null, "stock": [12, 2, 14, 3, 8, 18, 17, 10, 5, 16]}, "phase": 1, "p2_points": 0, "signature": null, "leads_turn": true};
testState = {"p1_points": 0, "player1s_turn": true, "revoked": null, "p1_pending_points": 0, "p2_pending_points": 0, "deck": {"trick": [null, 12], "trump_suit": "D", "p1_perspective": ["U", "U", "U", "P1H", "P1H", "S", "U", "U", "U", "P1H", "P1H", "U", "P2H", "U", "U", "U", "U", "P1H", "U", "U"], "card_state": ["S", "P2H", "S", "P1H", "P1H", "S", "S", "S", "P2H", "P1H", "P1H", "S", "P2H", "S", "P2H", "S", "P2H", "P1H", "S", "S"], "signature": null, "previous_trick": [null, null], "p2_perspective": ["U", "P2H", "U", "U", "U", "S", "U", "U", "P2H", "U", "U", "U", "P2H", "U", "P2H", "U", "P2H", "U", "U", "U"], "stock": [5, 19, 2, 11, 18, 15, 13, 6, 7, 0]}, "phase": 1, "p2_points": 0, "signature": null, "leads_turn": false};
state1 = {"p1_points": 0, "player1s_turn": true, "revoked": null, "p1_pending_points": 0, "p2_pending_points": 0, "deck": {"trick": [null, null], "trump_suit": "H", "p1_perspective": ["U", "U", "P1H", "U", "P1H", "U", "U", "U", "U", "P1H", "U", "P1H", "P1H", "U", "S", "U", "U", "U", "U", "U"], "card_state": ["S", "S", "P1H", "S", "P1H", "P2H", "S", "P2H", "P2H", "P1H", "P2H", "P1H", "P1H", "S", "S", "S", "S", "P2H", "S", "S"], "signature": null, "previous_trick": [null, null], "p2_perspective": ["U", "U", "U", "U", "U", "P2H", "U", "P2H", "P2H", "U", "P2H", "U", "U", "U", "S", "U", "U", "P2H", "U", "U"], "stock": [14, 0, 18, 13, 6, 19, 3, 1, 15, 16]}, "phase": 1, "p2_points": 0, "signature": null, "leads_turn": true};
state2 = {"p1_points": 0, "player1s_turn": false, "revoked": null, "p1_pending_points": 0, "p2_pending_points": 0, "deck": {"trick": [4, null], "trump_suit": "H", "p1_perspective": ["U", "U", "P1H", "U", "P1H", "U", "U", "U", "U", "P1H", "U", "P1H", "P1H", "U", "S", "U", "U", "U", "U", "U"], "card_state": ["S", "S", "P1H", "S", "P1H", "P2H", "S", "P2H", "P2H", "P1H", "P2H", "P1H", "P1H", "S", "S", "S", "S", "P2H", "S", "S"], "signature": null, "previous_trick": [null, null], "p2_perspective": ["U", "U", "U", "U", "P1H", "P2H", "U", "P2H", "P2H", "U", "P2H", "U", "U", "U", "S", "U", "U", "P2H", "U", "U"], "stock": [14, 0, 18, 13, 6, 19, 3, 1, 15, 16]}, "phase": 1, "p2_points": 0, "signature": null, "leads_turn": false};
state3 = {"p1_points": 6, "player1s_turn": true, "revoked": null, "p1_pending_points": 0, "p2_pending_points": 0, "deck": {"trick": [null, null], "trump_suit": "H", "p1_perspective": ["U", "U", "P1H", "U", "P1W", "U", "U", "P1W", "U", "P1H", "U", "P1H", "P1H", "U", "S", "U", "P1H", "U", "U", "U"], "card_state": ["S", "S", "P1H", "S", "P1W", "P2H", "S", "P1W", "P2H", "P1H", "P2H", "P1H", "P1H", "S", "S", "P2H", "P1H", "P2H", "S", "S"], "signature": null, "previous_trick": [4, 7], "p2_perspective": ["U", "U", "U", "U", "P1W", "P2H", "U", "P1W", "P2H", "U", "P2H", "U", "U", "U", "S", "P2H", "U", "P2H", "U", "U"], "stock": [14, 0, 18, 13, 6, 19, 3, 1]}, "phase": 1, "p2_points": 0, "signature": null, "leads_turn": true};
initialCardSetup(deck, testState);
// deck.cards.forEach(function(card){
//     card.setSide('front');
// })
