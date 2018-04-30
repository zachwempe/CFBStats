import re

header_string = '''Game#,Date,Opp,P-Cmp,P-Att,P-Pct,P-Yds,P-TD,R-Att,R-Yds,R-Avg,R-TD,T-Plays,T-Yds,T-Avg,1D-P,1D-R,1D-Pen,1D-Tot,Pen-No,Pen-Yds,Fum,Int,TO-Tot,Loc,Team-Pts,Opp-Pts,DP-Cmp,DP-Att,DP-Yds,DP-TD,DR-Att,DR-Yds,DR-Avg,DR-TD,DT-Plays,DT-Yds,DT-Avg,D1D-P,D1D-R,D1D-Pen,D1D-Tot,DPen-No,DPen-Yds,DFum,DInt,DTO-Tot'''

def clean_list(dirty_list):

    new_list = []

    for i in range(0, len(dirty_list)):
        loc_flag = str(0) # 0 if home, 1 if neutral, 2 if away
        stats_list = dirty_list[i].split('\t')
        if 'N' in stats_list:
            stats_list.remove('N')
            loc_flag = str(1)
        elif '@' in stats_list:
            stats_list.remove('@')
            loc_flag = str(2)
        else:
            stats_list.remove('')
        stats_list.append(loc_flag)
        stats_list[2] = re.sub('[*]','',stats_list[2])
        result = stats_list[3]
        del stats_list[3]
        split_result = result.split(' ')
        victory = split_result[0]
        scores = split_result[1].split('-')
        team_score = scores[0][1:]
        opp_score = scores[1][:-1]
        stats_list[-2] = stats_list[-2].rstrip()
        stats_list.append(team_score)
        stats_list.append(opp_score)
        new_list.append(stats_list)

    return new_list

def write_game_list_to_csv(team_name, game_data):
    csv_obj = open(team_name+'_gamedata.csv','w+')
    csv_obj.write(header_string+'\n')
    for i in range(len(game_data)):
        csv_obj.write(game_data[i]+'\n')
    csv_obj.close()
    return

def main(team_name):
    file_obj = open('RawTextData/'+team_name+'.txt','r')
    weeks_list = file_obj.readlines()
    file_obj.close()
    offense_list = clean_list(weeks_list[1:15])
    defense_list = clean_list(weeks_list[17:31])
    for i in range(0, len(defense_list)):
        defense_list[i] = defense_list[i][3:-3]
    game_list = []
    for i in range(0, len(offense_list)):
        game = offense_list[i] + defense_list[i]
        game_list.append(game)
    for i in range(0, len(game_list)):
        game_list[i] = ','.join(game_list[i])
    write_game_list_to_csv(team_name, game_list)

if __name__ == '__main__':
    team_name = 'Alabama'
    main(team_name)
