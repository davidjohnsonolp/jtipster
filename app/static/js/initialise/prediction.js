var selections = new SelectionCollection();
var selectionView = new SelectionListView({ el: $('#selected-predictions'), collection: selections });
selections.fetch({ reset: true });

var predictions = new PredictionCollection();
var predctionView = new PredictionListView({ el: $('#predictions-by-market'), collection: predictions });
predctionView.selections = selections;
predictions.fetch({ reset: true });