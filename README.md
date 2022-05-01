# FoodDiary

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

I wrote this script to calculate approximate number of calories, proteins, fats & carbohydrates which I consume during a day. 

I know that there is a lot of tools to solve this task. I tried to use many of them, but gave up eventually. Why? Well, some of them lose my data without an obvious reason, some have really terrible UI, and almost every one tries to sell me paid subscription. Gosh, I just need one simple function!

So I decide:

![Fine, I'll do it myself](tanos.png)

## How to use it? 

There are two YAML files: [catalog](catalog.yaml) of food you used to consume and [journal](journal.yaml) of products you have eaten.

For instance, you have eaten two apples for a lunch. If it's first time you eat an apple, you open catalog.yaml and write something like:  

```yaml
apple: 
  calories: 54
  protein:  0.4
  fat:      0.4
  carbs:    9.8
```

Then you open journal.yaml and write the name of food you just added to the catalog and its weights in grams:

```yaml
27.04.2022:

  - apple: 114
  - apple: 129
```

First line here is a current date. The journal may consist of many of them.  

After that, it's possible to execute [calc.py](calc.py) and see how many calories and macronutrients I've consumed:

```
py calc.py --profile=profile.yaml --journal=journal.yaml --catalog=catalog.yaml --weights=weights.yaml
```

For instance, script output may look like this:

```
FOOD                             CALORIES        PROTEIN         FAT             CARBS          

dumplings                        674             29              30              71             
bombarr                          377             40              13              4              
apple                            371             3               3               67             
whey                             186             36              3               3              
eggs                             182             15              13              1              
crab meat                        119             5               2               21             
tomato juice                     61              0               0               14             
white yogurt                     55              3               2               5              

TOTAL                            2025            131             66              186            

Balance today                                    34%             17%             49%            
Target ranges                                    45%             25%             30%            

Daily calorie intake — 1802 kcal; excess — 223!
```

## How to set up?

You can find all configurable parameters in the [profile.yaml](profile.yaml).  

## Which requirements does it have?

All dependencies are listed in [requirements.txt](requirements.txt).