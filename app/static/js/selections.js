var Selection = Backbone.Model.extend({ idAttribute: "id" });

var SelectionCollection = Backbone.Collection.extend({
    model: Selection,
    key: 'prediction-selections',

    fetch: function (options) {
        if (typeof (Storage) !== "undefined") {
            this.set(JSON.parse(localStorage.getItem(this.key)));
        }
    },

    save: function (attributes) {
        localStorage.setItem(this.key, JSON.stringify(this.toJSON()));
    },

    destroy: function (options) {
        localStorage.removeItem(this.key);
        //this.fetch();
    }
});

var SelectionListItemView = Backbone.View.extend({
    template: _.template(Templates.selectionListItem()),

    render: function () {
        var json = this.model.toJSON();
        json.KickOff = Globalize.format(new Date(json.KickOff), 'ddd, dd/MM/yyyy', 'en-GB');

        var html = this.template(json);
        this.setElement($(html));
        return this;
    }
});

var SelectionListView = Backbone.View.extend({
    initialize: function () {
        this.collection.bind("add", this.render, this);
        this.collection.bind("remove", this.render, this);
        this.collection.bind("reset", this.render, this);

        Backbone.mediator.on('odds-settings-changed', this.render, this);
    },

    events: {
        'click .delete': 'removePrediction',
        'change #accumulator-stake': 'setAccumulatorReturn',
        'keyup #accumulator-stake': 'setAccumulatorReturn',
        'click h2': 'setResponsiveDisplay',
        'click #add-to-my-bets': 'addToMyBets'
    },

    render: function () {
        this.$el.find('tbody').empty();

        if (this.collection.length > 0) {
            var oddsSetting = new OddsSetting();
            this.collection.each(function (prediction) {
                prediction.set('DisplayOdds', oddsSetting.getOdds(prediction.get('OddsDecimal')));
                
                var view = new SelectionListItemView({ model: prediction });
                var tr = view.render().$el;
                tr.toggleClass("invalid", !this.isValidSelection(prediction));

                this.appendPrediction(tr);
            }, this);
        }

        this.$el.toggleClass('responsive-hidden', this.collection.length == 0);

        this.$el.find('tbody').each(function (index, container) {
            if ($(container).is(':empty')) {
                $(container).html('<tr><td colspan="3">No selections.</td></tr>');
            }
        });

        this.$el.find('h2').text('Selections (' + this.collection.length + ')');

        var oddsSetting = new OddsSetting();
        this.$el.find('#combined-odds').text(oddsSetting.getOdds(this.getCombinedOdds()) + ' - ' + this.getBetLabel());

        this.setAccumulatorReturn();

        return this;
    },

    appendPrediction: function (predictionElement) {
        var predictionContainer = this.$el.find('table tbody');
        predictionContainer.append(predictionElement);
    },

    isValidSelection: function (prediction) {
        return new Date(prediction.get("KickOff")).setHours(0, 0, 0, 0) >= new Date().setHours(0, 0, 0, 0);
    },

    removePrediction: function (e) {
        var id = $(e.currentTarget).attr('data-id');
        this.collection.remove(this.collection.get(id));
        this.collection.save();

        $('input[id="' + id + '"]').click();

        this.setAccumulatorReturn();
    },
    
    getCombinedOdds: function () {
        var combinedOdds = 0;
        this.collection.each(function (prediction) {
            if (this.isValidSelection(prediction)) {
                var predictionOdds = prediction.get("OddsDecimal");

                if (predictionOdds > 0) {
                    if (combinedOdds == 0)
                        combinedOdds = predictionOdds;
                    else
                        combinedOdds *= predictionOdds;
                }
            }
        }, this);
        return combinedOdds;
    },
    
    getBetLabel: function() {
        switch(this.collection.length) {
            case 0: return "";
            case 1: return "single";
            case 2: return "double";
            case 3: return "treble";
            default: return this.collection.length + " folds";
        }
    },

    setAccumulatorReturn: function () {
        var combinedOdds = this.getCombinedOdds(),
            stake = parseFloat($('#accumulator-stake').val()),
            accumulatorReturn = 0;

        if (stake) {
            accumulatorReturn = stake.toFixed(2) * combinedOdds;
        }

        $('#accumulator-return').text("£" + (accumulatorReturn > 0 ? accumulatorReturn.toFixed(2) : "0.00"));
    },

    setResponsiveDisplay: function () {
        $('#selected-predictions').toggleClass('selected', 500);
    },
    
    addToMyBets: function(e) {
        e.preventDefault();

        if (!userAuthorized) {
            window.location.href = "Account/LogOn?next=%2fpredictions";
            return;
        }

        if(this.collection.length == 0){
            alert("Please enter at least one prediction.");
            return;
        }

        var stake = $('#accumulator-stake').val();
        if (!stake || parseFloat(stake) <= 0) {
            alert('Please enter a stake.');
            return;
        }

        var bet = new Bet();
        bet.set('stake', parseFloat(stake).toFixed(2));
        this.collection.each(function(prediction) {
            bet.addLine(prediction);
        });

        var _this = this;
        bet.save(bet.attributes, {
            success:function(model, response) {
                alert('Your bet has been saved. Visit the "my bets" page to track the result.');
                _this.clearBets();
                // trigger render of predictions
            },
            error: function(model, error) {
                alert('There has been a problem with your request. Please try again.');
            }
        });
    },

    clearBets: function() {
        this.collection.reset();
        this.collection.save();
        $('#accumulator-stake').val('');
        $('input:checkbox').removeAttr('checked');
    }
});

