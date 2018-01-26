// Removes all cards that are not needed to play Schnapsen
function schnapsenDeck(){
    fullDeck = Deck();
    fullDeck.cards.forEach(function (card) {
        if(card.rank<10 && card.rank>1){
            card.unmount();
        }
    });
    return fullDeck
}

// Get container
var $container = document.getElementById('container');

// Create Deck
var deck = schnapsenDeck();

// Add container to DOM
deck.mount($container);

deck.cards.forEach(function (card, i) {
    card.setSide('front');
	
    // Explode
    card.animateTo({
        delay: 1000 + i * 2, // wait 1 second + i * 2 ms
        duration: 500,
		ease: 'quartOut',
        
        x: Math.random() * window.innerWidth - window.innerWidth / 2,
        y: Math.random() * window.innerHeight - window.innerHeight / 2
    });
});