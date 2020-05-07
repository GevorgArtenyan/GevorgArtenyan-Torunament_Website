from .models import MatchModel, PlayerLeagueModel, GameModel
from django.db.models import F
from collections import OrderedDict, Counter
from django.db.models import Q

def table(player_list, game_list):
    player_point_dict = {}
    player_games_played_dict = {}
    player_wins_dict = {}
    player_draw_dict = {}
    player_defeat_dict = {}
    player_goal_scored = {}
    player_goal_conceded = {}
    player_goal_difference = {}
    for p in player_list:
        player_point_dict[str(p.pk)] = 0
        player_games_played_dict[str(p.pk)] = 0
        player_wins_dict[str(p.pk)] = 0
        player_draw_dict[str(p.pk)] = 0
        player_defeat_dict[str(p.pk)] = 0
        player_goal_scored[str(p.pk)] = 0
        player_goal_conceded[str(p.pk)] = 0
        player_goal_difference[str(p.pk)] = 1

    # Calculating the points of players. Every victory is 3 points, every draw is 1.
    for m in game_list:
        if m.h_score != None and m.a_score != None:
            player_games_played_dict[str(m.home_player.pk)] += 1
            player_games_played_dict[str(m.away_player.pk)] += 1
            player_goal_scored[str(m.home_player.pk)] += m.h_score
            player_goal_conceded[str(m.home_player.pk)] += m.a_score
            player_goal_scored[str(m.away_player.pk)] += m.a_score
            player_goal_conceded[str(m.away_player.pk)] += m.h_score

            if m.h_score > m.a_score:
                player_point_dict[str(m.home_player.pk)] += 3
                player_wins_dict[str(m.home_player.pk)] += 1
                player_defeat_dict[str(m.away_player.pk)] += 1
            elif m.h_score < m.a_score:
                player_point_dict[str(m.away_player.pk)] += 3
                player_wins_dict[str(m.away_player.pk)] += 1
                player_defeat_dict[str(m.home_player.pk)] += 1
            elif m.h_score == m.a_score:
                player_point_dict[str(m.home_player.pk)] += 1
                player_point_dict[str(m.away_player.pk)] += 1
                player_draw_dict[str(m.home_player.pk)] += 1
                player_draw_dict[str(m.away_player.pk)] += 1

    for k, v in player_point_dict.items():
        PlayerLeagueModel.objects.filter(pk=k).update(points=v)

    for k, v in player_wins_dict.items():
        PlayerLeagueModel.objects.filter(pk=k).update(wins=v)

    for k, v in player_draw_dict.items():
        PlayerLeagueModel.objects.filter(pk=k).update(draws=v)

    for k, v in player_defeat_dict.items():
        PlayerLeagueModel.objects.filter(pk=k).update(defeats=v)

    for k, v in player_games_played_dict.items():
        PlayerLeagueModel.objects.filter(pk=k).update(games_played=v)

    for k, v in player_goal_scored.items():
        PlayerLeagueModel.objects.filter(pk=k).update(goals_scored=v)

    for k, v in player_goal_conceded.items():
        PlayerLeagueModel.objects.filter(pk=k).update(goals_conceded=v)

    for k, v, in player_goal_scored.items():
        for ck, cv in player_goal_conceded.items():
            if k == ck:
                v -= cv
                player_goal_difference[k] = v

    for k, v in player_goal_difference.items():
        PlayerLeagueModel.objects.filter(pk=k).update(goal_difference=v)

def match_calc(game):
    match_dict = {}
    for g in game:
        match_dict[g.match.pk] = {g.match.player1.pk:0, g.match.player2.pk:0}

    for g in game:
        if g.h_score != None and g.a_score != None:
            match_dict[g.match.pk][g.home_player.pk] += g.h_score
            match_dict[g.match.pk][g.away_player.pk] += g.a_score

    for match_pk, match in match_dict.items():
        this_match = MatchModel.objects.get(pk=match_pk)
        MatchModel.objects.filter(pk=match_pk).update(score1=match[this_match.player1.pk],
                                          score2=match[this_match.player2.pk])

        if match[this_match.player1.pk] > match[this_match.player2.pk]:
            MatchModel.objects.filter(pk=this_match.pk).update(winner=this_match.player1)
            MatchModel.objects.filter(pk=this_match.pk).update(loser=this_match.player2)
        elif match[this_match.player1.pk] < match[this_match.player2.pk]:
            MatchModel.objects.filter(pk=this_match.pk).update(winner=this_match.player2)
            MatchModel.objects.filter(pk=this_match.pk).update(loser=this_match.player1)
        else:
            MatchModel.objects.filter(pk=this_match.pk).update(winner=None)
            MatchModel.objects.filter(pk=this_match.pk).update(loser=None)



def head_to_head_winner(player1, player2):
    try:
        match = MatchModel.objects.get(
            Q(player1=player1, player2=player2) |
            Q(player1=player2, player2=player1)
        )
        return match.winner
    except:
        match = None


def head_to_head_loser(player1, player2):
    match = MatchModel.objects.get(
        Q(player1=player1, player2=player2) |
        Q(player1=player2, player2=player1)
    )
    return match.loser




def sort_table(player_list):
    points_list = []
    for p in player_list:
        points_list.append(p)
    points_list.sort(key=lambda x: x.points, reverse=True)
    equal_point_players = []
    couples_list = []
    no_dub_couples = []
    sorted_by_head_to_head = []
    i = 0
    while i < len(points_list):
        j = 0
        while j < len(points_list):
            if points_list[i] != points_list[j] and points_list[i].points == points_list[j].points:
                if points_list[j] not in equal_point_players:
                    equal_point_players.append(points_list[j])
                    x = 0
                    while x < len(equal_point_players):
                        z = 0
                        while z < len(equal_point_players):
                            if equal_point_players[x] != equal_point_players[z] and equal_point_players[x].points == equal_point_players[z].points:
                                couples_list.append([equal_point_players[x], equal_point_players[z]])
                            z +=1
                        x +=1
                    for c in couples_list:
                        c.sort(key=lambda x: x.pk, reverse=True)
                    for nd in couples_list:
                        if nd not in no_dub_couples:
                            no_dub_couples.append(nd)
            j +=1
        i +=1
    for m in no_dub_couples:
        sorted_by_head_to_head.append(head_to_head_winner(m[0], m[1]))
        print(f'{m[0]} vs {m[1]} ----------> {head_to_head_winner(m[0], m[1])}')

    for p in player_list:
        if p.tournament.position_priority == 'Head to Head Matches':
            points_list.sort(key=lambda x: (x.points, sorted_by_head_to_head.count(x), x.goal_difference, x.goals_scored, x.wins), reverse=True)
        else:
            points_list.sort(key=lambda x: (x.points, x.goal_difference, sorted_by_head_to_head.count(x), x.goals_scored, x.wins), reverse=True)
    print(f'no_dub_couples - {no_dub_couples}')
    print(f'sprted_by_head_to_head - {sorted_by_head_to_head}')
    print(f'points_list - {points_list}')
    my_dict = {i: sorted_by_head_to_head.count(i) for i in sorted_by_head_to_head}
    print(my_dict)
    return points_list


