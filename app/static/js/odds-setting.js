var OddsSetting = Backbone.Model.extend({
    defaults: {
        odds: 'decimal'
    },
    
    key: 'odds',

    initialize: function () {
        if (typeof (Storage) !== "undefined") {
            this.set(JSON.parse(localStorage.getItem(this.key)));
        }
    },

    save: function (attributes) {
        localStorage.setItem(this.key, JSON.stringify(this.toJSON()));
    },

    destroy: function (options) {
        localStorage.removeItem(this.key);
    },
    
    getOdds: function(oddsDecimal) {
        var oddsType = this.get('odds');
        
        if (oddsType == "fractional") {
            var oddsAsString = oddsDecimal.toString();
            if (this.oddsMappings[oddsAsString]) {
                return this.oddsMappings[oddsAsString];
            }
            
            if (oddsDecimal < 2) {
                var numerator = parseInt(((oddsDecimal - 1) * 100).toFixed(0)),
                    commonDivisor = this.gcd(numerator, 100);

                return (numerator / commonDivisor) + "/" + (100 / commonDivisor);
            }

            return oddsDecimal ? (oddsDecimal - 1).toFixed(2).replace('.00', '') + "/1" : '';
        }

        return oddsDecimal.toFixed(2);
    },
    
    gcd: function(a, b) {
        if ( ! b) {
            return a;
        }

        return this.gcd(b, a % b);
    },
    
    oddsMappings: {
        "1.12": "1/8",
        "1.14": "1/7",
        "1.18": "2/11",
        "1.2": "1/5",
        "1.22": "2/9",
        "1.25": "1/4",
        "1.29": "2/7",
        "1.3": "30/100",
        "1.33": "1/3",
        "1.36": "4/11",
        "1.4": "2/5",
        "1.42": "21/50",
        "1.44": "4/9",
        "1.53": "8/15",
        "1.57": "4/7",
        "1.61": "8/13",
        "1.62": "8/13",
        "1.66": "4/6",
        "1.72": "8/11",
        "1.8": "4/5",
        "1.83": "5/6",
        "1.91": "10/11",
        "1.95": "19/20",
        "2.1": "11/10",
        "2.2": "6/5",
        "2.25": "5/4",
        "2.38": "11/8",
        "2.4": "7/5",
        "2.5": "6/4",
        "2.6": "8/5",
        "2.63": "13/8",
        "2.75": "7/4",
        "2.8": "9/5",
        "2.86": "15/8",
        "3.2": "11/5",
        "3.25": "9/4",
        "3.4": "12/5",
        "3.5": "5/2",
        "3.6": "13/5",
        "3.75": "11/4",
        "4.33": "100/30",
        "4.5": "7/2",
        "5.5": "9/2",
        "6.5": "11/2",
        "7.5": "13/2",
        "8.5": "15/2",
        "9.5": "17/2",
        "1.47": "40/85",
        "2.05": "21/20",
        "3.13": "85/40"
    }
});

var OddsSettingView = Backbone.View.extend({

    render: function () {
        var id = this.model.get('odds');
        $('input[data-Id="' + id + '"]').prop('checked', true);

        return this;
    },
    
    events: {
        'change #odds-display-decimal': 'saveSettingsOptions',
        'change #odds-display-fractional': 'saveSettingsOptions'
    },
    
    saveSettingsOptions: function (e) {
        var id = $(e.currentTarget).attr('data-Id');
        this.model.set('odds', id);
        this.model.save();
        
        Backbone.mediator.trigger('odds-settings-changed');
    }
});