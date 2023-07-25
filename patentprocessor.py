from urllib import request
from bs4 import BeautifulSoup
import requests
import urllib.request
import requests, zipfile, io
import os
import pandas as pd

# Change this to include all needed year paths
year_paths = ["/Users/lawrenceliu/Dropbox (MIT)/All Patent Data/2018",
              "/Users/lawrenceliu/Dropbox (MIT)/All Patent Data/2019",
              "/Users/lawrenceliu/Dropbox (MIT)/All Patent Data/2020",
              "/Users/lawrenceliu/Dropbox (MIT)/All Patent Data/2021",
              "/Users/lawrenceliu/Dropbox (MIT)/All Patent Data/2022",
              "/Users/lawrenceliu/Dropbox (MIT)/All Patent Data/2023"]

for path in year_paths:
    # repeat for each year

    year = path[-4:]

    # split the year's patent issues into different file paths
    all_issues = os.listdir(path)
    all_issues_paths = [os.path.join(path,issue,"OG/geographical") for issue in all_issues if issue[0] != "."]

    # Dictionaries to eventually be turned into pandas dataframes, sorted by year
    df = pd.read_csv("cpccodescsv.csv")
    all_cpc_codes = df["codes"].tolist()
    all_state_abbrv = df["Abbrv"].tolist()[:50]
    all_cpc_codes.extend(df["Dcodes"].tolist()[:33])
    all_cpc_codes.append("PLT")

    cpc_frequencies = {code: [0 for i in range(51)] for code in all_cpc_codes}
   
    # lookup dictionaries for states and indices
    number_to_state = {}
    state_to_number = {}
    for i in range(50):
        number_to_state[i] = all_state_abbrv[i]
        state_to_number[all_state_abbrv[i]] = i

    # Add misc categories
    all_state_abbrv.append("Other")
    all_cpc_codes.append("F24J")
    number_to_state[50] = "Other"
    state_to_number["Other"] = 50

    # repeat following process for each issue
    for issue_path in all_issues_paths:
        all_states = os.listdir(issue_path)
        all_states_paths = []

        # split by state
        # find all relevant "STATE_XXBODY.html" pages
        for statehtmlname in all_states:
            if statehtmlname[:4] == "STAT" and statehtmlname[-9:] == "Body.html":
                all_states_paths.append(os.path.join(issue_path,statehtmlname))
        
        # Repeat for each state
        for state_path in all_states_paths:
            # Put html page into Soup
            with open(state_path,"r") as f:
                soup = BeautifulSoup(f,"html.parser")
            
            # Isolate only the subclass, subgroup, and patent columns from the selection table
            table = soup.find_all(name = "td", attrs = {"align":"left"})
            state = state_path[state_path.index("STATE") + 6:state_path.index("STATE") + 8]
            last_code = ""

            for element in table:
                strippedelement = str(element.text).strip()
                if strippedelement in ["Subclass", "Subgroup","Patent", "Class"]:
                    pass
                elif strippedelement in all_cpc_codes:
                    last_code = strippedelement
                elif "/" in strippedelement:
                    pass
                else:
                    try:
                        # check design or regular
                        # if a patent or a design subclass

                        intstrippedelement = int(strippedelement)

                        # Design subclass are all 3 digit numbers
                        if intstrippedelement <1000:
                            pass

                        # Utility patent numbers are all large numbers
                        if state not in all_state_abbrv:
                            # other, us territory
                            cpc_frequencies[last_code][50]+=1
                        else:
                            # add to appropriate state count
                            cpc_frequencies[last_code][state_to_number[state]]+=1
                    except:
                        if state not in all_state_abbrv:
                            # other, us territory
                            cpc_frequencies[last_code][50]+=1
                        else:
                            # add to appropriate state count
                            cpc_frequencies[last_code][state_to_number[state]]+=1

    # Export the data into a csv with columns as states and rows as CPC classification codes
    # New file per year, labeled year.csv for respective year frequencies
    pd.DataFrame.from_dict(cpc_frequencies, orient="index",columns = all_state_abbrv).to_csv("/Users/lawrenceliu/Dropbox (MIT)/final/"+str(year)+".csv")
    







