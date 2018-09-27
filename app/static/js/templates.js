var Templates = {};

Templates.selectionListItem = function () {
    return '<tr> \
                <td class="odds"> \
                    <%= DisplayOdds %> \
                </td> \
                <td> \
                    <em><%= Name %></em> \
                    <%= HomeTeamName %> vs <%= AwayTeamName %> \
                </td> \
                <td> \
                    <a class="delete button" data-id="<%= id %>"> \
                        <span class="hidden">Delete</span> \
                    </a> \
                    <input type="hidden" value="<%= id %>" /> \
                </td> \
            </tr>';
};

Templates.predictionListItem = function () {
    return '<tr> \
                <td><input type="checkbox" id="<%= id %>" /></td> \
                <td class="kick-off"><%= KickOff %></td> \
                <td> \
                    <em><%= Name %></em> \
                    <%= HomeTeamName %> vs <%= AwayTeamName %> \
                </td> \
                <td class="odds"> \
                    <%= DisplayOdds %> \
                </td> \
            </tr>';
};

Templates.betListItem = function () {
    return '<tr id="bet-<%= id %>"> \
                <td> \
                    <ol> \
                    </ol> \
                </td> \
                <td class="responsive-hidden"> \
                    <%= CombinedOdds %> \
                </td> \
                <td> \
                    <%= DisplayStake %> \
                </td> \
                <td> \
                    <%= DisplayReturns %> \
                </td> \
                <td> \
                    <a class="delete button" data-id="<%= id %>"> \
                </td> \
            </tr>';
};

Templates.betLineItem = function() {
    return '<li> \
                <em><%= Name %> (<%= Status %>)</em>  \
                <%= HomeTeamName %> vs <%= AwayTeamName %> \
                <span><%= DisplayOdds %></span> \
            </li>';

};

Templates.extractItem = function() {
    return '<tr> \
                <td> \
                    <%= name %> \
                </td> \
                <td> \
                    <button data-id="<%= id %>">Update</button> \
                </td> \
            </tr>';
};

Templates.tipItem = function() {
    return '<tr id="<%= id %>"> \
                    <td> \
                        <em> \
                            <%= HomeTeamName %> \
                            vs  \
                            <%= AwayTeamName %> \
                        </em> \
                        <span><%= KickOff %></span> \
                        <span><%= Competition %></span> \
                        \
                        <a class="stats-link">Stats</a> \
                        <div class="stats-content"> \
                            <div> \
                                <em><%= HomeTeamName %></em> \
                                <%= HomeMatches %> \
                            </div> \
                            <div> \
                                <em><%= AwayTeamName %></em> \
                                <%= AwayMatches %> \
                            </div> \
                        </div> \
                    </td> \
                    \
                    <td> \
                        <ul> \
                            <li> \
                                <label>Market</label> \
                                <select class="market"> \
                                    <option value="0">Full Time Result</option> \
                                    <option value="1">Total Match Goals</option> \
                                    <option value="2">Asian Handicap</option> \
                                    <option value="3">Full Time Result and Total Match Goals</option> \
                                    <option value="4">Full Time Result and BTTS</option> \
                                    <option value="5">Total Match Goals and BTTS</option> \
                                </select> \
                            </li> \
                            <li> \
                                <label>Selection</label> \
                                <select class="market-participant"> \
                                    <option value="0"><%= HomeTeamName %> win</option> \
                                    <option value="1"><%= HomeTeamName %> draw no bet</option> \
                                    <option value="2"><%= HomeTeamName %> win or draw</option> \
                                    <option value="3"><%= AwayTeamName %> win</option> \
                                    <option value="4"><%= AwayTeamName %> draw no bet</option> \
                                    <option value="5"><%= AwayTeamName %> win or draw</option> \
                                    <option value="6">Over</option> \
                                    <option value="7">Under</option> \
                                    <option value="8"><%= HomeTeamName %> win and over</option> \
                                    <option value="9"><%= AwayTeamName %> win and over</option> \
                                    <option value="10">Over and yes</option> \
                                </select> \
                            </li> \
                            <li> \
                                <label>Threshold</label> \
                                <input class="threshold" type="number" value="<%= MarketParticipantThreshold %>" /> \
                            </li> \
                            <li> \
                                <label>Odds</label> \
                                <input class="odds-decimal" type="number" value="<%= OddsDecimal %>" /> \
                            </li> \
                            <li> \
                                <label>Status</label> \
                                <select class="status"> \
                                    <option value="0">Unknown</option> \
                                    <option value="1">Pending</option> \
                                    <option value="2">Win</option> \
                                    <option value="3">Lose</option> \
                                    <option value="4">Void</option> \
                                </select> \
                            </li> \
                        </ul> \
                    </td> \
                    <td>\
                        <a class="delete button" data-id="<%= id %>"> \
                        <a class="update button" data-id="<%= id %>"> \
                        </a> \
                    </td>\
                </tr>';
};
