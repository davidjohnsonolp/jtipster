var leagues = new LeagueExtractCollection();
var extractView = new LeagueExtractListView({ el: $('#extract'), collection: leagues });
leagues.fetch({ reset: true });