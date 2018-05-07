from lxml import html
import requests
import sys


header_string = '''Game#,Date,Opp,P-Cmp,P-Att,P-Pct,P-Yds,P-TD,R-Att,R-Yds,R-Avg,R-TD,T-Plays,T-Yds,T-Avg,1D-P,1D-R,1D-Pen,1D-Tot,Pen-No,Pen-Yds,Fum,Int,TO-Tot,Loc,Team-Pts,Opp-Pts,DP-Cmp,DP-Att,DP-Yds,DP-TD,DR-Att,DR-Yds,DR-Avg,DR-TD,DT-Plays,DT-Yds,DT-Avg,D1D-P,D1D-R,D1D-Pen,D1D-Tot,DPen-No,DPen-Yds,DFum,DInt,DTO-Tot'''

def get_list(tree, side):
    
    stat_list = []
    i = 1
    row = tree.xpath('//table[@id="%s"]//tr//th[@csk="%d"]//..//text()' % (side, i))
    while len(row) != 0:
        loc_flag = str(0)

        if 'N' in row:
            row.remove('N')
            loc_flag = str(1) # 0 if home, 1 if neutral, 2 if away
        elif '@' in row:
            row.remove('@')
            loc_flag = str(2)
        row.append(loc_flag)
        if '*' in row:
            row.remove('*')
        result = row[3]
        del row[3]
        split_result = result.split(' ')
        victory = split_result[0]
        scores = split_result[1].split('-')
        team_score = scores[0][1:]
        opp_score = scores[1][:-1]
        row[-2] = row[-2].rstrip()
        row.append(team_score)
        row.append(opp_score)
        stat_list.append(row)
        i += 1
        row = tree.xpath('//table[@id="%s"]//tr//th[@csk="%d"]//..//text()' % (side, i))
    return stat_list


def write_game_list_to_csv(team_name, game_data):

    csv_obj = open('../2017TeamStats/'+team_name+'_gamedata.csv','w+')
    csv_obj.write(header_string+'\n')
    for i in range(len(game_data)):
        csv_obj.write(game_data[i]+'\n')
    csv_obj.close()
    return


def main(team_name):

    page = requests.get("https://www.sports-reference.com/cfb/schools/alabama/2017/gamelog/")
    string = page.text
    string = string.replace('<!--\n','')
    string = string.replace('\n-->','')
    tree = html.fromstring(string)
    offense_list = get_list(tree, "offense")
    defense_list = get_list(tree, "defense")
    for i in range(0, len(defense_list)):
        defense_list[i] = defense_list[i][3:-3]
    game_list = []
    for i in range(0, len(offense_list)):
        game = offense_list[i] + defense_list[i]
        game_list.append(game)
    for i in range(0, len(game_list)):
        game_list[i] = ','.join(game_list[i])
    write_game_list_to_csv(team_name, game_list)
    return



if __name__ == '__main__':
    main(sys.argv[1])
