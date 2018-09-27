var LeagueExtract = Backbone.Model.extend({
    idAttribute: 'id',
    urlRoot: '/api/leagues'
});

var LeagueExtractCollection = Backbone.Collection.extend({
    url: '/api/leagues',
    model: LeagueExtract,

    parse: function (response) {
        return response.extracts;
    }
});

var LeagueExtractListItemView = Backbone.View.extend({
    template: _.template(Templates.extractItem()),

    events: {
        "click button": "callExtractor"
    },

    render: function () {
        var html = this.template(this.model.toJSON());
        this.setElement($(html));
        return this;
    },

    callExtractor: function(e){
        var url = "/api/leagues" + this.model.get("id");
        var target = $(e.currentTarget).prop('disabled', true).addClass("extracting").text(''),
            output = $('#live-update-status').empty();

        this.model.save({}, {
                success: function(model, response, options) {
                    target.removeClass("extracting").removeClass("error").addClass("extracted")
                    output.append('Number of predictions: ' + response.predictions.length + '<br /><br />Log Trace...')
                    for (var l in response.log){
                        output.append('<br />' + response.log[l]);
                    }

                    if (response.predictions.length > 0)
                        console.log(response.predictions);
                },
                error: function (model, response, options){
                    target.prop('disabled', false).removeClass("extracting").addClass("error").text('Try Again')
                    output.text(options.xhr.responseText)
                }
        });
    }
});

var LeagueExtractListView = Backbone.View.extend({
    initialize: function () {
        this.collection.bind("reset", this.render, this);
    },

    render: function () {
        var tbody = this.$el.find('#leagues-data tbody');
        tbody.empty();

        if (this.collection.length > 0) {
            this.collection.each(function (extract) {
                var view = new LeagueExtractListItemView({ model: extract });
                var tr = view.render().$el;

                if (extract.get("enabled"))
                    tbody.append(tr);
            });
        }

        this.$el.find('#leagues-data tbody').each(function (index, container) {
            if ($(container).is(':empty')) {
                $(container).html('<tr><td>No league data was found.</td></tr>');
            }
        });

        return this;
    }
});