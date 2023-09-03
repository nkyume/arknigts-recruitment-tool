import itertools
from time import sleep
import dbfunctions as db
from tags_extractor import extract
from scrapper import update_operators_data
import os

colors = {
        'white': '\033[1;37m',
        'green': '\033[0;32m',
        'blue': '\033[0;34m',
        'grey': '\033[0;37m',
        'yellow': '\033[1;33m',
        'orange': '\033[38;5;208m',
        'pink': '\033[38;5;218m',
        'purple': '\033[0;35m',
        'nocolor': '\33[0m'
        }

def main():
    if input('Update operators list? (y/n): ') == 'y':
        update_operators_data()
    
    while True:
        is_top_operator = False 
        tags = extract(db.available_tags(), "BlueStacks App Player")
        # Flag for Top Operator tag
        if "Top Operator" in tags:
            is_top_operator = True
            
        combinatons = combine_tags(tags, 3)
        avalible_operators = sorted(get_avalible_operators(combinatons, is_top_operator), key=lambda d: d["combination_min_rarity"])
        
        # Console output
        for tag_combination in avalible_operators:
            tags_color = color_set(tag_combination['combination_min_rarity'])
            print(f"{tags_color}{tag_combination['combination_min_rarity']}* {tag_combination['combination']}{colors['nocolor']}")
            
            for operator in tag_combination['operators']:
                if operator['name'] == 'Melantha':
                    operator_color = colors['purple']
                else:
                    operator_color = color_set(operator['rarity'])
                print(f"{operator_color}{operator['name']} {operator['rarity']}* | {colors['nocolor']}", end="")    
            print("\n")  
             
        sleep(5)
    
      
def color_set(rarity):   
    color = None
    match rarity:
        case 1:
            color = colors['grey']
        case 2:
            color = colors['green']
        case 3:
            color = colors['blue']
        case 4:
            color = colors['pink']
        case 5:
            color = colors['yellow']
        case 6:
            color = colors['orange']
        case _:
            color = colors['white']
    return color


def get_avalible_operators(combinatons, is_top_operator):
    avalible_operators = []
    
    for combi in combinatons:
        
        combi = "%".join(combi)
        operators_raw = db.retrieve_operators_by_tags(f"%{combi}%")
        combi = combi.replace('%', ', ')
        if not operators_raw:
            continue
        operators = []
        min_rarity = 0
        raritys = []
        
        # Get rid of 6* operators if no top tag
        for operator in operators_raw:
            if operator[1] == 6 and not is_top_operator:
                continue
            
            tmp_operator = {
                'name': operator[0],
                'rarity': operator[1],
                'tags': operator[2],
                #'image': operator[3]    
            }
            operators.append(tmp_operator)
            raritys.append(tmp_operator["rarity"])
        if not raritys:
               continue
        if set(raritys) == {1}:
            min_rarity = 1
        elif set(raritys) == {2}:
            min_rarity = 2
        elif set(raritys) == {6}:
            min_rarity = 6
        else:
            min_rarity = min(raritys)
            if min_rarity < 3:
                min_rarity = 3

        tmp_tags = {
            'combination': combi,
            'combination_min_rarity': min_rarity,
            'operators': operators,   
        }    
          
        avalible_operators.append(tmp_tags)
    return avalible_operators    

                 
def combine_tags(tags, times):
    """
    Return combinations of all tags 
    """
    combination = []
    tmp = []
    for i in range(1, times + 1):
        tmp += itertools.combinations(tags, i)
    for combi in tmp:
        combination.append(sorted(list(combi)))
    return combination


if __name__ == "__main__":
    main()
    
