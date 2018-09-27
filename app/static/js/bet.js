var Bet = Backbone.Model.extend({
    idAttribute: 'id',
    urlRoot: '/api/bet',
    defaults: {},

    initialize: function() {
        var returns = 0.00,
            isWinner = true,
            lines = this.get('lines'),
            stake = this.get('stake'),
            combinedOdds = 1,
            oddsSetting = new OddsSetting();

        if (lines){
            for (var i = 0; i < lines.length; i++) {
                if (lines[i].Status != 2) {
                    isWinner = false;
                }
                combinedOdds *= lines[i].OddsDecimal;
            }
        }
        if (isWinner) {
            returns = combinedOdds * this.get('stake');
        }

        this.set('CombinedOdds', oddsSetting.getOdds(combinedOdds));
        this.set('Returns', returns);
        this.set('DisplayReturns', "£" + returns.toFixed(2));
        this.set('DisplayStake', "£" + (stake ? stake.toFixed(2) : "0.00"));
    },

    addLine: function(line) {
        var lines = this.get('lines');
        if (!lines) {
            lines = new Array();
        }

        lines.push(line);
        this.set('lines', lines);
    }
});

var BetCollection = Backbone.Collection.extend({
    url: '/api/bet',
    model: Bet,

    parse: function (response) {
        return response.bets;
    },

    initialize: function() {
        this.sortKey = 'timestamp';
    },

    comparator: function(bet) {
        return -bet.get(this.sortKey);
    }
});

var BetItemLineView = Backbone.View.extend({
    template: _.template(Templates.betLineItem()),

    initialize: function(){
        var oddsSetting = new OddsSetting();

        this.model.set({ DisplayOdds: oddsSetting.getOdds(this.model.get('OddsDecimal')) });
    },

    render: function(){
        var html = this.template(this.model.toJSON());
        this.setElement($(html));

        return this;
    }
});

var BetItemView = Backbone.View.extend({
    template: _.template(Templates.betListItem()),

    events: {
        "click .delete": "deleteBet"
    },
    
    render: function () {
        var html = this.template(this.model.toJSON());
        this.setElement($(html));

        _.each(this.model.get('lines'), function(line){
            var lineView = new BetItemLineView({ model: new Prediction(line) });
            this.$el.find('ol').append(lineView.render().$el);
        }, this);

        return this;
    },

    deleteBet: function (e){
        if (confirm("Are you sure you want to delete this bet?")){
            var el = this.$el, _this = this;
            this.model.destroy({
                success : function(model, response) {
                    if (response.success) {
                        el.fadeOut({
                            complete: function () {
                                el.remove();
                                _this.collection.reset(_this.collection.models);
                            }
                        });
                    }
                    else alert('Selection not found. Please refresh.');
                },
                error : function(model, response) {
                    alert('There has been a problem with your request. Please try again.');
                }
            });
        }
    }
});

var BetView = Backbone.View.extend({

    initialize: function () {
        this.collection.bind("reset", this.render, this);

        Backbone.mediator.on('odds-settings-changed', this.render, this);
    },

    render: function () {
        this.$el.find('#my-bets-data tbody').empty();

        if (this.collection.length > 0) {
            var totalStake = 0.00,
                totalReturn = 0.00;
            
            this.collection.each(function (bet) {
                var view = new BetItemView({ model: bet, collection: this.collection });
                var tr = view.render().$el;
                this.appendBet(tr);

                totalStake += bet.get("stake");
                totalReturn += bet.get("Returns");

            }, this);

            $('#total-stake').text('£' + totalStake.toFixed(2));
            $('#total-return').text('£' + totalReturn.toFixed(2));
        }

        this.$el.find('#my-bets-data tbody').each(function (index, container) {
            if ($(container).is(':empty')) {
                $(container).html('<tr><td colspan="5">You have no saved bets.</td></tr>');
            }
        });

        return this;
    },

    appendBet: function (betElement) {
        var betContainer = this.$el.find('table tbody');
        betContainer.append(betElement);
    }
});