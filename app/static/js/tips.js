var Tip = Backbone.Model.extend({
    idAttribute: 'id',
    urlRoot: '/api/tip'
});

var TipCollection = Backbone.Collection.extend({
    url: '/api/tip',
    model: Tip,

    parse: function (response) {
        return response.tips;
    }
});

var TipListItemView = Backbone.View.extend({
    template: _.template(Templates.tipItem()),

    events: {
        "click .stats-link": "toggleStatsDisplay",
        "click .delete": "deleteTip",
        "click .update": "updateTip"
    },

    render: function () {
        var html = this.template(this.model.toJSON());
        this.setElement($(html));

        this.$el.find('.market').val(this.model.get('MarketType'));
        this.$el.find('.market-participant').val(this.model.get('MarketParticipantType'));
        this.$el.find('.status').val(this.model.get('Status'));

        return this;
    },

    toggleStatsDisplay: function() {
        this.$el.find('.stats-content').animate({ height: "toggle" }, 1000);
    },

    deleteTip: function (e){
        if (confirm("Are you sure you want to delete this tip?")){
            var el = this.$el;
            this.model.destroy({
                success : function(model, response) {
                    if (response.success) {
                        el.fadeOut({
                            complete: function () {
                                el.remove();
                            }
                        });
                    }
                    else alert('Selection not found. Please refresh.');
                    console.log(result);
                },
                error : function(model, response) {
                    alert('There has been a problem with your request. Please try again.');
                }
            });
        }
    },

    updateTip: function (e) {
        this.model.save({
            MarketType: parseInt(this.$el.find('.market').val()),
            MarketParticipantType: parseInt(this.$el.find('.market-participant').val()),
            MarketParticipantThreshold: parseFloat(this.$el.find('.threshold').val()),
            OddsDecimal: parseFloat(this.$el.find('.odds-decimal').val()),
            Status: parseInt(this.$el.find('.status').val())
        },
        {
            success: function (model, response){
                if (response.success) {
                    alert('Selection updated successfully.');
                }
                else alert('Selection not found. Please refresh.')
            },
            error: function (model, response){
                alert('There has been a problem with your request. Please try again.');
            }
        });
    }
});

var TipListView = Backbone.View.extend({
    initialize: function () {
        this.collection.bind("reset", this.render, this);
    },
    events: {
        "click #update-all-tips": "updateTips"
    },

    render: function () {
        var tbody = this.$el.find('#tips-data tbody');
        tbody.empty();

        if (this.collection.length > 0) {
            this.collection.each(function (tip) {
                var view = new TipListItemView({ model: tip });
                var tr = view.render().$el;
                tbody.append(tr);
            });
        }

        tbody.find('#tips-data tbody').each(function (index, container) {
            if ($(container).is(':empty')) {
                $(container).html('<tr><td colspan="3">No tip data was found.</td></tr>');
            }
        });

        return this;
    }
});