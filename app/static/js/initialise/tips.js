var tips = new TipCollection();
var tipsView = new TipListView({ el: $('#tips'), collection: tips });
tips.fetch({ reset: true });