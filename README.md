# FoodDiary

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Этот инструмент я использую для примерного расчета количества калорий, которые я получил за день, а также контроля за балансом БЖУ (белков, жиров и углеводов)

Знаю, есть целый выводок приложений для решения этой задачи, но мне не нравится ни одно из них: какое-то теряет данные, где-то неудобный интерфейс, и почти все назойливо пытаются всучить платную подписку. А мне нужна одна-единственная простая функция!

## Как использовать? 

В течении дня я записываю в дневник (`meals.yaml`) всё, что съел.

Пример:

```yaml
- Яблоко, 130
```

Если за день я съел что-то, чего раньше не ел — добавляю информацию об этом продукте или блюде в справочник (`foods.yaml`). Там хранится калорийность и количество белков-жиров-углеводов на сто грамм.

Пример:

```yaml
Яблоко: {
    К: 40,      # калорийность
    Б: 0.4,     # содержание белков
    Ж: 0.4,     # содержание жиров
    У: 9.8      # содержание углеводов
}
```

Когда я хочу понять, не перевалил ли за норму калорий в сутки и соблюдается ли баланс БЖУ — запускаю скрипт вывода статистики (`scripts/print_meals.py`). Он отображает:

1. Остаток калорий на сегодня;
2. Общую калорийность в разрезе съеденных продуктов;
3. Количество белков, жиров и углеводов для каждого съеденного продукта;
4. Процентное соотношение всех потребленных в течении дня белков, жиров и углеводов.

Пример:

```
ПРОДУКТ                                       К          Б          Ж          У         

Вареная ветчина "Семейная"                    306        24         21         5         
Сосиски "Восточные"                           121        10         9          0         
Яблоко                                        56         1          1          14        

ИТОГО                                         483        35         31         19        

БАЛАНС БЖУ СЕГОДНЯ                                       41%        36%        22%       
ЦЕЛЕВОЙ БАЛАНС БЖУ                                       30%        20%        50%       

Дневная норма — 1650 ккал; остаток на сегодня — 1167.
```

Кроме этого, каждое утро я запускаю скрипт создания нового дневника (`scripts/clear_meals.py`) — он создает копию дневника в папке `history`, а потом очищает его.

## Как настроить? 

Настройка делается через файл `settings.yaml`. В нем можно задать дневной лимит калорий, имя директории для архивных дневников, имя файла дневника и имя файла справочника.

Пример:

```yaml
calories_limit:   1650          # дневной лимит калорий
archive_dirname:  'history'     # имя директории с архивом дневников
journal_filename: 'meals.yaml'  # имя файла дневника
catalog_filename: 'foods.yaml'  # имя файла справочника
```