import datetime
from pathlib import Path
import sys

def posOrAsk(i, prompt):
    try:
        return sys.argv[i]
    except IndexError:
        return input(prompt)

if __name__ == '__main__':
    category = posOrAsk(1, 'Category? ')
    title = posOrAsk(2, 'Title? ')
    try:
        priority = sys.argv[3]
    except IndexError:
        priority = '00'
    
    rt = Path('.')
    (rt / 'docs' / category).mkdir(parents=True, exist_ok=True)
    (rt / 'docs' / category / (title + '.md')).touch()

    t = datetime.date.today()
    with open(rt / 'docs' / category / (title + '.txt'), 'w', encoding='utf-8') as f:
        f.write('{} {:0>4d} {:0>2d} {:0>2d}'.format(priority, t.year, t.month, t.day))
    