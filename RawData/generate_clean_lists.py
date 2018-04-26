'''
Simple script to clean copy-pasted lists of fbs and fcs teams
Lists copied from http://www.espn.com/college-football/teams
'''

def fcs_list_clean():
    fcs_file_obj = open('FCSTeams.txt','r')
    fcs_list = fcs_file_obj.readlines()
    fcs_file_obj.close()
    fcs_list_split = []
    for entry in fcs_list:
        split_entry = entry.split('     ')
        fcs_list_split.append(split_entry)
    fcs_list_clean = []
    for entry in fcs_list_split:
        if len(entry) > 1:
            fcs_list_clean.append(entry[0] + '\n')
    write_file = open('FCSTeams.txt','w')
    write_file.writelines(fcs_list_clean)
    write_file.close()


def fbs_list_clean():
    fbs_file_obj = open('FBSTeams.txt','r')
    fbs_list = fbs_file_obj.readlines()
    fbs_file_obj.close()
    fbs_list_split = []
    for entry in fbs_list:
        split_entry = entry.split('     ')
        fbs_list_split.append(split_entry)
    fbs_list_clean = []
    for entry in fbs_list_split:
        if len(entry) > 1:
            fbs_list_clean.append(entry[0] + '\n')
    write_file = open('FBSTeams.txt','w')
    write_file.writelines(fbs_list_clean)
    write_file.close()

def main():
    fcs_list_clean()
    fbs_list_clean()

if __name__ == '__main__':
    main()
