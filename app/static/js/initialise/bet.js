var bets = new BetCollection();
var betsView = new BetView({ el: $('#bets'), collection: bets });
bets.fetch({ reset: true });
