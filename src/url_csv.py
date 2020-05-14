import sys
sys.path.append("..")

import src.key_reader as kr
api_key = kr.key()

 
def halftime_team_report(api_key=api_key):
    """
    input: api key (str)
    output: csv file saved in the data folder
    """
    
    import time
    import requests
    from pathlib import Path
    import pandas as pd
    
    """
    CALL LIMITS FOR RIOT GAMES API

    20 calls per second
    
    100 calls per 120 seconds
        
    input: api key (list)
    output: pandas dataframe
    """
    
    # Requesting match IDs 
    
    with open('../data/matchlist_kr.json','r') as file:
        match_ids = json.load(file)
    
    api_error_n = 0
    
    
    for match_id in match_ids:
    
        if n % 45 == 0:
            time.sleep(125)
            pass
          
        response_match = requests.get(f'https://kr.api.riotgames.com/lol/match/v4/matches/{match_id}?api_key={api_key}')

        n += 1

        a = response_match.json()

        team1_halftime_stats = {'match_id': match_id}

        team2_halftime_stats = {'match_id': match_id}

        try:
            ## Adding additional ingame data
            halftime_stats = []

            for team_i in range(len(a['teams'])):
                if a['teams'][team_i]['teamId'] == 100:
                    team1_halftime_stats['teamId'] = 1
                    team1_halftime_stats['win'] = a['teams'][team_i]['win']
                    team1_halftime_stats['firstBlood'] = a['teams'][team_i]['firstBlood']
                    team1_halftime_stats['firstTower'] = a['teams'][team_i]['firstTower']
                    team1_halftime_stats['firstInhibitor'] = a['teams'][team_i]['firstInhibitor']
                    team1_halftime_stats['firstBaron'] = a['teams'][team_i]['firstBaron']
                    team1_halftime_stats['firstDragon'] = a['teams'][team_i]['firstDragon']
                    team1_halftime_stats['firstRiftHerald'] = a['teams'][team_i]['firstRiftHerald']

                else:
                    team2_halftime_stats['teamId'] = 2
                    team2_halftime_stats['win'] = a['teams'][team_i]['win']
                    team2_halftime_stats['firstBlood'] = a['teams'][team_i]['firstBlood']
                    team2_halftime_stats['firstTower'] = a['teams'][team_i]['firstTower']
                    team2_halftime_stats['firstInhibitor'] = a['teams'][team_i]['firstInhibitor']
                    team2_halftime_stats['firstBaron'] = a['teams'][team_i]['firstBaron']
                    team2_halftime_stats['firstDragon'] = a['teams'][team_i]['firstDragon']
                    team2_halftime_stats['firstRiftHerald'] = a['teams'][team_i]['firstRiftHerald']
                        
            halftime_stats.append(team1_halftime_stats)
            halftime_stats.append(team2_halftime_stats)
            
            # Checking if a csv file exists before appending the data
            my_file = Path("../data/ht_match.csv")

            # Create a csv file if it does not exist
            if not my_file.is_file():
                match_stats_df = pd.DataFrame(halftime_stats)
                match_stats_df.to_csv('../data/ht_match.csv')
                time.sleep(0.125)
                halftime_stats = []
            # Append data onto the existing csv file
            else:
                match_stats_df = pd.DataFrame(halftime_stats)
                match_stats_df.to_csv('../data/ht_match.csv',header=None,mode='a')
                time.sleep(0.125)
                halftime_stats = []
        

        except:
            print(response_match.status_code)
            print(f"n'th match: {n}")
            print(api_error_n)
            api_error_n += 1

            if (response_match.status_code == 429) and api_error_n < 3:
                time.sleep(30)
                pass

            elif (response_match.status_code == 429) and api_error_n >= 3 and api_error_n < 7:
                time.sleep(30)
                pass

            elif api_error_n >= 7:
                print('breaking due to excessive number of pulls')
                break
            
            elif response_match.status_code == 504 or response_t.status_code == 503:
                api_error_n -=1
                time.sleep(30)
                pass
            
            else:
                print(response_match.status_code)
                time.sleep(30)
                pass

def halftime_individual(api_key = api_key):
    """
    input: api key (str)
    output: csv file saved in the data folder
    """
    import requests
    import pandas as pd
    import json
    import time
    from pathlib import Path

    with open('../data/matchlist_kr.json','r') as file:
        match_ids = json.load(file)

    api_error_n = 0

    for match_id in match_ids:

        if n % 45 == 0:
            time.sleep(130)
            pass

        response_t = requests.get(f'https://kr.api.riotgames.com/lol/match/v4/timelines/by-match/{match_id}?api_key={api_key}')
        n += 1
        
        b = response_t.json()

        #keys = ['participantId','totalGold','level','xp','killerId','victimId']
        keys = ['totalGold','level','xp','totalKills','totalDeaths']

        team1_halftime_stats = {'match_id': match_id,'totalGold':0,'level':0,
                                'xp':0,'totalKills':0,'totalDeaths':0, 'level_ups':0}

        team2_halftime_stats = {'match_id': match_id,'totalGold':0,'level':0,
                                'xp':0,'totalKills':0,'totalDeaths':0, 'level_ups':0}

        try:
            # Taking first half of the match stats to predict the match outcome.
            for frame_i in range(len(b['frames'])//2):

                ## Grabbing ingame gold, levels, xp    
                for p_i in range(1,len(participant_ids)+1):
                    for ind_key in keys[:-2]:
                        if b['frames'][frame_i]['participantFrames'][str(p_i)]['participantId'] <= 5:
                            team1_halftime_stats[ind_key] += b['frames'][frame_i]['participantFrames'][str(p_i)][ind_key]
                        else:
                            team2_halftime_stats[ind_key] += b['frames'][frame_i]['participantFrames'][str(p_i)][ind_key]

                ## Grabbing ingame kills and deaths
                for event_i in range(len(b['frames'][frame_i]['events'])):
                    for ind_key2 in keys[-2:]:

                        if b['frames'][frame_i]['events'][event_i]['type'] == 'CHAMPION_KILL':
                            if b['frames'][frame_i]['events'][event_i]['killerId'] <= 5:
                                team1_halftime_stats['totalKills'] += 1
                                team2_halftime_stats['totalDeaths'] += 1
                            else:
                                team2_halftime_stats['totalKills'] += 1
                                team1_halftime_stats['totalDeaths'] += 1       
                        if b['frames'][frame_i]['events'][event_i]['type'] =='SKILL_LEVEL_UP':
                            if b['frames'][frame_i]['events'][event_i]['participantId'] <= 5:
                                team1_halftime_stats['level_ups'] += 1
                            else:
                                team2_halftime_stats['level_ups'] += 1
            
            halftime_stats = []
            halftime_stats.append(team1_halftime_stats)
            halftime_stats.append(team2_halftime_stats)

            # Checking if a csv file exists before appending the data
            my_file = Path("../data/ht_match_ind.csv")

            # Create a csv file if it does not exist
            if not my_file.is_file():
                match_stats_df = pd.DataFrame(halftime_stats)
                match_stats_df.to_csv('../data/ht_match_ind.csv')
                time.sleep(0.125)
                halftime_stats = []
            # Append data onto the existing csv file
            else:
                match_stats_df = pd.DataFrame(halftime_stats)
                match_stats_df.to_csv('../data/ht_match_ind.csv',header=None,mode='a')
                time.sleep(0.125)
                halftime_stats = []
        except:
            print(api_error_n)
            api_error_n += 1
            print(f"error occurred in n'th match: {n}")
            print(f"API status code: {response_t.status_code}")

            if response_t.status_code == 429 and api_error_n < 3:
                time.sleep(30)
                pass

            elif response_t.status_code == 429 and api_error_n >= 3 and api_error_n < 10:
                time.sleep(30)
                pass

            elif api_error_n >= 10:
                print('breaking due to excessive number of pulls')
                break

            elif response_t.status_code == 504 or response_t.status_code == 503:
                time.sleep(30)
                api_error_n -= 1
                pass
            else:
                time.sleep(30)
                pass        
            
def df_join(df1,df2):
    
    # Removing curly brackets from the match IDs
    df1['match_id'] = df1['match_id'].apply(lambda x: x[1:-1])
    
    df1 = df1.rename(columns = {'Unnamed: 0':'teams'})
    df2 = df2.rename(columns = {'Unnamed: 0':'teams'})
    
    
    