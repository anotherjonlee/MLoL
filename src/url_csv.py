def seed_csv():
    """
    This function extracts seed match data from the developer's s3 bucket
    and converts and saves as a csv file
    
    input:  none
    output: returns a pandas dataframe
    """
    import json
    import requests
    import pandas as pd
    from pathlib import Path

    ## Extracting from all 10 seed match data
    key_list = []

    match_stats_list = []

    for num in range(1,11):
        
        r = requests.get(url = f'https://s3-us-west-1.amazonaws.com/riot-developer-portal/seed-data/matches{num}.json')
        match_details = r.json()
        
        # check for and set up keys
        if len(key_list) < 1:
            for i in match_details['matches'][0]['participants'][0]['stats'].keys():
                key_list.append(i)
        
        # Remove unnecessary features
        if len(key_list) > 61:
            ind_dict_keys = key_list[:-14]
        
        # populate match_stats_list 
        for match_i in range(len(match_details['matches'])) :
            
            for participant_i in range(len( match_details['matches'][match_i]['participants'])):
                match_stats_dict = {}
                
                for key in ind_dict_keys:
                    try:
                        match_stats_dict[key] = match_details['matches'][match_i]['participants'][participant_i]['stats'][key]
                    except:
                        if not key in ind_dict_keys:
                            match_stats_dict[key] = None
                match_stats_list.append(match_stats_dict)
    
    # Converting the list to a pandas dataframe before saving it as a csv file
    my_file = Path("../data/seed_data.csv")
    
    if not my_file.is_file():
        match_stats_df = pd.DataFrame(match_stats_list)
        match_stats_df.to_csv('../data/seed_data.csv')    
        
    return match_stats_df

def api_csv(key_list, key, region, match_ids):
    import json
    import requests
    import pandas as pd
    from pathlib import Path



def halftime_report(match_ids, api_key=api_key):
    import time
    import requests
    from pathlib import Path
    import pandas as pd
    
    """
    CALL LIMITS FOR RIOT GAMES API

    20 calls per second
    
    100 calls per 120 seconds
    
    60,000 calls per 10 minutes (600 seconds)
    
    input: api key (list)
    output: pandas dataframe
    """
    
    # Requesting match IDs 
    
    #r = requests.get(url = 'http://canisback.com/matchId/matchlist_kr.json')   
    #match_ids = r.json()
    
    n = 0
    
    api_error_n = 0
    
    for match_id in match_ids:
    
        if n % 2 == 0:
            time.sleep(4)
            pass
        
        if n % 15 == 0:
            time.sleep(10)
            pass
        
        elif n% 35 == 0:
            time.sleep(60)
            pass
        
        elif n % 70 == 0:
            time.sleep(120)
            pass
        
        elif n % 110 == 0:
            time.sleep(300)
            pass
    
        elif n % 130 == 0:
            time.sleep(500)
            pass
        
        elif n % 235 == 0:
            time.sleep(600)
            pass
        
        response_match = requests.get(f'https://kr.api.riotgames.com/lol/match/v4/matches/{match_id}?api_key={api_key}')
        response_t = requests.get(f'https://kr.api.riotgames.com/lol/match/v4/timelines/by-match/{match_id}?api_key={api_key}')

        n += 2

        a = response_match.json()
        b = response_t.json()

        keys = ['totalGold','level','xp','totalKills','totalDeaths']

        team1_halftime_stats = {'match_id': '4366059781','totalGold':0,'level':0,
                                'xp':0,'totalKills':0,'totalDeaths':0, 'level_ups':0}

        team2_halftime_stats = {'match_id': '4366059781','totalGold':0,'level':0,
                                'xp':0,'totalKills':0,'totalDeaths':0, 'level_ups':0}

        # Taking first half of the match stats to predict the match outcome.
        try:
            halftime_stats = []

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

            ## Adding additional ingame data
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
            #match_stats_df = pd.DataFrame(halftime_stats)

            # Create a csv file if it does not exist
            if not my_file.is_file():
                match_stats_df = pd.DataFrame(halftime_stats)
                match_stats_df.to_csv('../data/ht_match.csv')
                time.sleep(10)

            # Append data onto the existing csv file
            else:
                match_stats_df = pd.DataFrame(halftime_stats)
                match_stats_df.to_csv('../data/ht_match.csv',header=None,mode='a')
                time.sleep(10)
        except:
            print(response.status_code)
            print(n)

            api_error_n += 1

            if response.status_code == 429 and api_error_n < 3:
                time.sleep(300)
                pass

            elif response.status_code == 429 and temp_n >= 3 and api_error_n < 7:
                time.sleep(500)
                pass

            elif api_error_n >= 7:
                print('breaking due to excessive number of pulls')
                break

            else:
                print('other api issues')
                break

    print('scraping complete')