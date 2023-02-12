# 🍞 🍏 🥩 Food Diary

[![PyPi](https://img.shields.io/pypi/v/foodlog)](https://pypi.org/project/foodlog/) [![pylint](https://github.com/vkostyanetsky/Foodlog/actions/workflows/pylint.yml/badge.svg)](https://github.com/vkostyanetsky/Foodlog/actions/workflows/pylint.yml) [![black](https://github.com/vkostyanetsky/Foodlog/actions/workflows/black.yml/badge.svg)](https://github.com/vkostyanetsky/Foodlog/actions/workflows/black.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This script calculates approximate number of calories, proteins, fats & carbohydrates which I consume during a day. 

Of course, I'm aware that there are countless tools to solve the task, on smartphones especially. Furthermore, I've tried to use many of them, but gave up eventually. Some of them lose my data without a reason, some have terrible UI, and almost each one dreams of selling me a paid subscription. Gosh, I just need one simple function!

So I decide:

![Fine, I'll do it myself](https://github.com/vkostyanetsky/FoodDiary/raw/main/tanos.png)

## ☺ Installation

```
pip install foodlog 
```

## 🤔 How to use it? 

There are two YAML files: `catalog.yaml` which contains food you used to consume and `journal.yaml` which contains products you have eaten.

Let's imagine that today is March 27, and you have eaten two apples for a lunch. If it's first time you eat an apple, you open catalog.yaml and write something like:  

```yaml
apple: 
  calories: 54
  protein:  0.4
  fat:      0.4
  carbs:    9.8
```

Then you open journal.yaml and write the name of food you just added to the catalog and its weights in grams:

```yaml
2022-04-27:

- apple: 114
- apple: 129
```

First line here is a current date in the YYYY-MM-DD format. The journal may consist of many of them. For example:

```yaml
2022-04-26:
  
- apple: 120  
- bread: 403
- pizza: 356

2022-04-27:

- apple: 114
- apple: 129
```

Having catalog & journal both filled, it's possible to see how many calories and macronutrients you've consumed. Run this in a working directory:

```
foodlog
```

For instance, script output may look like this:

```
FOOD                   CALORIES        PROTEIN         FAT             CARBS           GRAMS          

peremech               539             22              31              45              198            
fish in batter         500             49              23              21              250            
ham                    361             54              13              9               361            
apples                 262             2               2               48              485            
yogurt                 228             11              9               26              190            
peach                  131             3               0               32              285            
watermelon             126             3               1               29              502            
sweet corn             82              3               0               18              163            
drinking water         0               0               0               0               800            

TOTAL                  2229            147             79              228                            

Balance today                          32%             17%             50%                            
Target ranges                          45%             25%             30%                            

Daily calorie intake is 1803 kcal; excess is 426!

Body weight dynamic:
- yesterday    109.1
- today        109.1
```

You can find all configurable parameters of the script (calories limit, target ranges of macronutrients etc.) in the `profile.yaml` file.

## 🧐 How can I take water I consume into account?

There are no calories & macronutrients in water. Consequently, you can add a record like this one to your `catalog.yaml` file:

```yaml
h2o:
  calories: 0
  protein:  0
  fat:      0
  carbs:    0
water: h2o
```

From this point, you can use these identifiers like other ones in your `journal.yaml` file. The script still shows you how much water you consume in the `GRAMS` column of daily statistics; for instance:

```yaml
FOOD                   CALORIES        PROTEIN         FAT             CARBS           GRAMS

apples                 157             1               1               28              290
ham                    103             11              4               6               124
water                  0               0               0               0               800
```

There is no balance value for a day, but you are free to decide what is your norm.

By the way, you may use this method to control your intake of other products which have no calories. Coffee, for instance. 