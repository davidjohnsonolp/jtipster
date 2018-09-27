var Prediction = Backbone.Model.extend({
    idAttribute: "id",

    initialize: function() {
        this.set("Name", this.getName());
    },

    getName: function(){
        var market = this.get("MarketType"),
            marketParticipant = this.get("MarketParticipantType"),
            threshold = this.get("MarketParticipantThreshold"),
            name = "";

        switch(market){
            case 0:
                switch(marketParticipant){
                    case 0: return this.get("HomeTeamName") + " to win";
                    case 1: return this.get("HomeTeamName") + " draw no bet";
                    case 2: return this.get("HomeTeamName") + " to win or draw";
                    case 3: return this.get("AwayTeamName") + " to win";
                    case 4: return this.get("AwayTeamName") + " draw no bet";
                    case 5: return this.get("AwayTeamName") + " to win or draw";
                }
            case 1:
                return "Match goals " + (marketParticipant == 6 ? "> " :"< ") + threshold.toFixed(1);
            case 2:
                switch(marketParticipant){
                    case 0: return this.get("HomeTeamName") + " " + threshold.toFixed(1);
                    case 3: return this.get("AwayTeamName") + " " + threshold.toFixed(1);
                }
            case 3:
                var team = marketParticipant == 8 ? this.get("HomeTeamName") : this.get("AwayTeamName");
                return team + " to win and match goals > " + threshold.toFixed(1);
        }
    }
});

var PredictionCollection = Backbone.Collection.extend({
    url: '/api/predictions',
    model: Prediction,

    initialize: function () {
        this.sortKey = 'KickOff';
    },

    comparator: function (prediction) {
        return -prediction.get(this.sortKey);
    },

    parse: function (response) {
        return response.predictions;
    }
});