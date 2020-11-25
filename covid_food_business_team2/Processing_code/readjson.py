import json

#file = "patterns-part2.csv.json"
def write_json(file,dic):
    with open(file) as f:
      data = json.load(f)
    lst = data["Boston"]


    for element in lst:
        temp = eval(element['popularity_by_day'])
        postal_code = element["postal_code"]
        if postal_code not in dic:
            dic[postal_code] = temp
        else:
            dic[postal_code]["Monday"] += temp["Monday"]
            dic[postal_code]["Tuesday"] += temp["Tuesday"]
            dic[postal_code]['Wednesday'] += temp['Wednesday']
            dic[postal_code]['Thursday'] += temp['Thursday']
            dic[postal_code]['Friday'] += temp['Friday']
            dic[postal_code]['Saturday'] += temp['Saturday']
            dic[postal_code]['Sunday'] += temp['Sunday']
    return dic
dic = {}
file_list =["patterns-part1.csv.json","patterns-part2.csv.json","patterns-part3.csv.json","patterns-part4.csv.json"]
for file in file_list:
    dic = write_json(file,dic)
jsonFilePath = "postal_code2.json"
with open(jsonFilePath, 'w+', encoding='utf-8') as jsonf:
    jsonf.write(json.dumps(dic, indent=4))