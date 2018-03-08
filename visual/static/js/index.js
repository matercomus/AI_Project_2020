// TODO

// Set better height/width for won cards
// Represent marriages/exchanges

// Maybe use the hardcoded card sizes to make sure cards never overlap

// Revisit dealStock - not sure what this means, old comment.

// Play around with transitions, everything looks really static currently.

// Implement one-hot encoding in ml.py

// Add some arg options to server.py, so the parameters are not hard coded.

// Maybe perform additional logical checks in order to avoid switching card sides so often

// Interactive mode - clickable cards:

// var a = deck.cards[50].$el
// undefined
// $(a)
// w.fn.init [div.card.diamonds.rank12]
// $(a).click(function(){
// alert("foo");})


// Removes all cards that are not needed to play Schnapsen
function schnapsenDeck(){
    fullDeck = Deck();
    fullDeck.cards.forEach(function (card) {
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
    new_cards_array = [];

    for(i=0; i<stock.length; i++){
        new_cards_array.push(visualDeck.backEndIndices[stock[i]]);
    }

    visualDeck.cards.forEach(function(card, index){
        if(new_cards_array.indexOf(card) < 0){
            new_cards_array.push(card);
        }
    });

    if(new_cards_array.length == visualDeck.cards.length){
        visualDeck.cards = new_cards_array;
    } else alert("Card ordering error");

    visualDeck.cards.forEach(function (card, index) {
        card.pos = index;
        card.$el.style.zIndex = card.pos;
    });

}

function arrangeCards(visualDeck, backEndState){
    p1placed = 0;
    p2placed = 0;
    p1wonCount=0;
    p2wonCount=0;

    var x = null;
    var y = null;

    var height = window.innerHeight;
    var width = window.innerWidth;

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

function setUpCards(visualDeck, backEndState){

    var height = window.innerHeight;
    var width = window.innerWidth;

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
}

function getCardStateArray(backEndState){
    card_state = backEndState.deck.card_state
    trick = backEndState.deck.trick

    for(i=0; i<2; i++){
        if(trick[i] != null){
            card_state[trick[i]] = "P" + parseInt(i+1) + "D";
        }
    }
    return card_state;
}

function stateFinished(state){
    if(state.revoked != null || state.p1_points >= 66 || state.p2_points >= 66){
        return true;
    }
    return false;
}

function startGameLoop(deck, state){

    setUpCards(deck, state);

    setTimeout(function(){

        if(stateFinished(state)){
            console.log("Game finished");
            return;
        }

        // Not using async request because it doesn't run on main thread
        $.ajax({
            url: '/next',
            type: 'GET',
            success: function(response) {
                startGameLoop(deck, JSON.parse(response));

            },
            error: function(error) {
                console.log(error);
                console.log("Error in game loop");
                return;
            }
        });

    }, INTERVAL);

}

var ordered = false;
var stateObject = null;

const INTERVAL = 1000;

// Get container
var $container = document.getElementById('container');

// Create Deck
var deck = schnapsenDeck();

// Add container to DOM
deck.mount($container);

$.ajax({
    url: '/generate',
    type: 'GET',
    success: function(response) {
        stateObject = JSON.parse(response);
        console.log(stateObject);
        startGameLoop(deck, stateObject);
    },
    error: function(error) {
        console.log(error);
    }
});
