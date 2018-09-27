var PredictionListItemView = Backbone.View.extend({
    template: _.template(Templates.predictionListItem()),
    events: {
    },
    render: function () {
        var json = this.model.toJSON();
        json.KickOff = Globalize.format(new Date(json.KickOff), 'ddd, dd/MM/yyyy HH:mm', 'en-GB');

        var html = this.template(json);
        this.setElement($(html));
        return this;
    }
});

var PredictionListView = Backbone.View.extend({
    selections: new SelectionCollection(),

    initialize: function () {
        this.collection.bind("reset", this.render, this);
        this.collection.bind("reset", this.populateDates, this);

        Backbone.mediator.on('odds-settings-changed', this.render, this);
    },

    events: {
        "click .fixtures tr": "rowClick",
        "change #filter-date": "render",
        "change .fixtures input": "updateSelections"
    },

    render: function () {
        this.$el.find('.fixtures tbody').empty();

        if (this.collection.length > 0) {
            var oddsSetting = new OddsSetting();
            this.collection.each(function (prediction) {
                prediction.set('DisplayOdds', oddsSetting.getOdds(prediction.get('OddsDecimal')));
                
                var view = new PredictionListItemView({ model: prediction });
                var tr = view.render().$el;
                tr.find('input').attr('checked', this.selections.get(prediction.get('id')) != null);

                if (this.isDateInRange(prediction))
                    this.appendPrediction(tr);

                var kickOffFormatted = Globalize.format(new Date(prediction.get('KickOff')), 'dddd - dd/MM/yyyy', 'en-GB');

                if ($("#filter-date option[value='" + kickOffFormatted + "']").length == 0) {
                    $('#filter-date').append($("<option/>", {
                        value: kickOffFormatted,
                        text: kickOffFormatted
                    }));
                }
            }, this);
        }

        this.$el.find('.fixtures tbody').each(function (index, container) {
            if ($(container).is(':empty')) {
                $(container).html('<tr><td colspan="4">No tips for this market at this time.</td></tr>');
            }
        });

        return this;
    },

    appendPrediction: function (predictionElement) {
        var predictionContainer = this.$el.find('table.fixtures tbody');
        predictionContainer.append(predictionElement);
    },

    rowClick: function (e) {
        if (e.target.tagName == 'INPUT') return;

        var input = $(e.currentTarget).find('input');
        input.click();
    },

    isDateInRange: function (prediction) {
        var selectedDateValue = $('#filter-date').val();
        return selectedDateValue == "ALL" || selectedDateValue == Globalize.format(new Date(prediction.get('KickOff')), 'dddd - dd/MM/yyyy', 'en-GB');
    },

    updateSelections: function () {
        this.selections.reset();

        var selectedPredictions = [], _this = this;
        this.$el.find('.fixtures tbody input').each(function (index, container) {
            var input = $(container);
            if (input.is(':checked')) {
                var id = input.attr('id');
                selectedPredictions.push(_this.collection.get(id));
            }
        });

        this.selections.add(selectedPredictions);

        this.selections.save();
    }
});
