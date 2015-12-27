import pandas as pd
import csv
from datetime import datetime

def careerLength(start, end):
    start = datetime.strptime(start, "%m/%d/%y")
    end = datetime.strptime(end, "%m/%d/%y")
    return abs((end-start).days)

class TreeNode(dict):
    def __init__(self, name, children=None):
        super(TreeNode, self).__init__()
        self.__dict__ = self
        self.name = name
        self.children = [] if not children else children
    def from_dict(dict_):
        root = TreeNode(dict_["name"], dict_["children"])
        root.children = list(map(TreeNode.from_dict, root.children))
        return root

#def store():
    
    
# def store(races, row):
#     name = row["Name"]
#     race = row["Race"]
#     nationality = row["Nationality"]
#     bestResult = row["Best result (totally biased selection)"]
#     length = careerLength(row["Career start"], row["Career end"])
#     player = {"name": name, "size": length, "bestResult": bestResult}
#     (races[race])[nationality].append(player)
    
data = pd.read_csv('careersData.csv')
tree = TreeNode("SC2 Career Stats")
for race in pd.unique(data.Race.ravel()):
    raceChild = TreeNode(race)
    tree.children.append(raceChild)
    raceData = data.loc[data["Race"] == race]
    for nationality in pd.unique(raceData.Nationality.ravel()):
        nationalityChild = TreeNode(nationality)
        raceChild.children.append(nationalityChild)
        
        nationalityData = raceData.loc[raceData["Nationality"] == nationality]
        playerData = nationalityData[["Name","Best result (totally biased selection)", "Career start", "Career end"]]
        for index, row in playerData.iterrows():
            nationalityChild.children.append({"name": row["Name"], "bestResult": "" if pd.isnull(row["Best result (totally biased selection)"]) else row["Best result (totally biased selection)"], "size": careerLength(row["Career start"], row["Career end"]), "active" : "True" if row["Career end"] == "12/31/15" else "False"})
        
import json
json_str = json.dumps(tree, sort_keys=True, indent=2, ensure_ascii=False)
#print(json_str)
f = open("readme.json", "w")
print >> f, json_str
f.close()
# races = {}
# nationalities = {}
# #create an nationality list for every race
# for nationality in pd.unique(data.Nationality.ravel()):
#     nationalities[nationality] = []
# for race in pd.unique(data.Race.ravel()):
#     races[race] = nationalities


# data.apply(lambda row: store(races, row), axis=1)

# import json
# with open("careersData.json", "w") as fp:
#     json.dump(races, fp, ensure_ascii=False)
#