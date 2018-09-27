from datetime import datetime
from models import Tip

def get_home_win_tips(home_team, away_team, competition, kickoff, match_history):
    tips = []
    sorted_matches = sorted(match_history, key=lambda match: match["date"], reverse=True)
    home_wins_form = get_home_wins_form_8_matches(home_team, competition, sorted_matches)
    away_loss_form = get_away_loss_form_8_matches(away_team, competition, sorted_matches)
    wins_form = get_wins_form_6_matches(home_team, competition, sorted_matches)
    loss_form = get_loss_form_6_matches(away_team, competition, sorted_matches)

    if home_wins_form >= 5 and away_loss_form >= 5 and (wins_form >= 4 or loss_form >= 4):
        home_description = "Home wins: %i/8.\nHome/Away wins: %i/6." % (home_wins_form, wins_form)
        away_description = "Away loss: %i/8.\nHome/Away loss: %i/6." % (away_loss_form, loss_form)

        tip = Tip(HomeTeamName=home_team,
                  AwayTeamName=away_team,
                  KickOff=kickoff,
                  MarketType=0,
                  MarketParticipantType=0,
                  Status=0,
                  LastUpdate=datetime.utcnow(),
                  Competition=competition,
                  HomeMatches=home_description,
                  AwayMatches=away_description)

        tips.append(tip)

    return tips

def get_away_win_tips(home_team, away_team, competition, kickoff, match_history):
    tips = []
    sorted_matches = sorted(match_history, key=lambda match: match["date"], reverse=True)
    away_wins_form = get_away_wins_form_8_matches(away_team, competition, sorted_matches)
    home_loss_form = get_home_loss_form_8_matches(home_team, competition, sorted_matches)
    wins_form = get_wins_form_6_matches(away_team, competition, sorted_matches)
    loss_form = get_loss_form_6_matches(home_team, competition, sorted_matches)

    if away_wins_form >= 5 and home_loss_form >= 5 and (wins_form >= 4 or loss_form >= 4):
        home_description = "Home loss: %i/8.\nHome/Away loss: %i/6." % (home_loss_form, loss_form)
        away_description = "Away wins: %i/8.\nHome/Away wins: %i/6." % (away_wins_form, wins_form)

        tip = Tip(HomeTeamName=home_team,
                  AwayTeamName=away_team,
                  KickOff=kickoff,
                  MarketType=0,
                  MarketParticipantType=3,
                  Status=0,
                  LastUpdate=datetime.utcnow(),
                  Competition=competition,
                  HomeMatches=home_description,
                  AwayMatches=away_description)

        tips.append(tip)

    return tips

def get_goals_over_tips(home_team, away_team, competition, kickoff, match_history, threshold=2.5):
    tips = []
    sorted_matches = sorted(match_history, key=lambda match: match["date"], reverse=True)
    home_overs_count = get_home_goals_over_form_8_matches(home_team, competition, sorted_matches, threshold)
    away_overs_count = get_away_goals_over_form_8_matches(away_team, competition, sorted_matches, threshold)
    home_overs_all_average = get_goals_over_average_6_matches(home_team, competition, sorted_matches)
    away_overs_all_average = get_goals_over_average_6_matches(away_team, competition, sorted_matches)

    average_threshold = threshold + 0.25
    if home_overs_count >= 5 and away_overs_count >= 5 and home_overs_all_average >= average_threshold and away_overs_all_average >= average_threshold:
        home_description = "Matches > 2.5 goals: %i/8.\nAverage goals over 6 matches: %.2f.\n" % (home_overs_count, home_overs_all_average)
        away_description = "Matches > 2.5 goals: %i/8.\nAverage goals over 6 matches: %.2f.\n" % (away_overs_count, away_overs_all_average)

        tip = Tip(HomeTeamName=home_team,
                  AwayTeamName=away_team,
                  KickOff=kickoff,
                  MarketType=1,
                  MarketParticipantType=6,
                  MarketParticipantThreshold=2.5,
                  Status=0,
                  LastUpdate=datetime.utcnow(),
                  Competition=competition,
                  HomeMatches=home_description,
                  AwayMatches=away_description)

        tips.append(tip)

    return tips

def get_home_wins_form_8_matches(home_team, competition, match_history):
    wins = 0
    competition_matches = filter(lambda match: match.get("hometeam/_title", "") == home_team
                                            and match.get("competition", "") == competition
                                            and has_result(match), match_history)

    for match in competition_matches[:8]:
        result = [int(x) for x in match["result"].split("-")]
        if result[0] > result[1]:
            wins += 1

    return wins

def get_away_loss_form_8_matches(away_team, competition, match_history):
    losses = 0
    competition_matches = filter(lambda match: match.get("awayteam/_title", "") == away_team
                                            and match.get("competition", "") == competition
                                            and has_result(match), match_history)

    for match in competition_matches[:8]:
        result = [int(x) for x in match["result"].split("-")]
        if result[0] > result[1]:
            losses += 1

    return losses

def get_away_wins_form_8_matches(away_team, competition, match_history):
    wins = 0
    competition_matches = filter(lambda match: match.get("awayteam/_title", "") == away_team
                                            and match.get("competition", "") == competition
                                            and has_result(match), match_history)

    for match in competition_matches[:8]:
        result = [int(x) for x in match["result"].split("-")]
        if result[0] < result[1]:
            wins += 1

    return wins

def get_home_loss_form_8_matches(home_team, competition, match_history):
    losses = 0
    competition_matches = filter(lambda match: match.get("hometeam/_title", "") == home_team
                                            and match.get("competition", "") == competition
                                            and has_result(match), match_history)

    for match in competition_matches[:8]:
        result = [int(x) for x in match["result"].split("-")]
        if result[0] < result[1]:
            losses += 1

    return losses

def get_wins_form_6_matches(team, competition, match_history):
    wins = 0

    competition_matches = filter(lambda match: (match.get("hometeam/_title", "") == team or match.get("awayteam/_title", "") == team)
                                            and match.get("competition", "") == competition
                                            and has_result(match), match_history)

    for match in competition_matches[:6]:
        result = [int(x) for x in match["result"].split("-")]
        if (result[0] > result[1] and match.get("hometeam/_title", "") == team) or (result[0] < result[1] and match.get("awayteam/_title", "") == team):
            wins += 1

    return wins

def get_loss_form_6_matches(team, competition, match_history):
    losses = 0

    competition_matches = filter(lambda match: (match.get("hometeam/_title", "") == team or match.get("awayteam/_title", "") == team)
                                            and match.get("competition", "") == competition
                                            and has_result(match), match_history)

    for match in competition_matches[:6]:
        result = [int(x) for x in match["result"].split("-")]
        if (result[0] > result[1] and match.get("awayteam/_title", "") == team) or (result[0] < result[1] and match.get("hometeam/_title", "") == team):
            losses += 1

    return losses

def get_home_goals_over_form_8_matches(home_team, competition, match_history, threshold):
    overs = 0
    competition_matches = filter(lambda match: match.get("hometeam/_title", "") == home_team
                                            and match.get("competition", "") == competition
                                            and has_result(match), match_history)

    for match in competition_matches[:8]:
        result = [int(x) for x in match["result"].split("-")]
        if result[0] + result[1] > threshold:
            overs += 1

    return overs

def get_away_goals_over_form_8_matches(away_team, competition, match_history, threshold):
    overs = 0
    competition_matches = filter(lambda match: match.get("awayteam/_title", "") == away_team
                                            and match.get("competition", "") == competition
                                            and has_result(match), match_history)

    for match in competition_matches[:8]:
        result = [int(x) for x in match["result"].split("-")]
        if result[0] + result[1] > threshold:
            overs += 1

    return overs

def get_goals_over_average_6_matches(team, competition, match_history):
    goals = 0.0
    competition_matches = filter(lambda match: (match.get("hometeam/_title", "") == team or match.get("awayteam/_title", "") == team)
                                            and match.get("competition", "") == competition
                                            and has_result(match), match_history)

    for match in competition_matches[:6]:
        result = [int(x) for x in match["result"].split("-")]
        goals += result[0] + result[1]

    return goals / 6

def has_result(match):
    result = match.get("result", "")
    return result != "" and result != "-" and result != "PSTP" and result != "CANC" and result.find(":") == -1