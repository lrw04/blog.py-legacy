from pathlib import Path
import os
import sys
import shutil

def grabjobs(wd):
    jobs = {}
    for category in wd.iterdir():
        if not category.is_dir(): continue
        jobs[category.parts[-1]] = []
        for article in category.iterdir():
            if article.parts[-1][-3:] == '.md':
                jobs[category.parts[-1]].append(article.parts[-1][:-3])
    return jobs

def readcfg(pth):
    return {
        'home': open(pth / 'home.html', encoding='utf-8').read(),
        'category': open(pth / 'category.html', encoding='utf-8').read(),
        'document': open(pth / 'document.html', encoding='utf-8').read(),
        'name': open(pth / 'name.txt', encoding='utf-8').read().strip()
    }

# Fix non-standard titles
def prep(s):
    r = ''
    doconv = True
    for line in s.splitlines():
        if len(line) > 2 and line[:3] == '```':
            doconv = not doconv
        if len(line) == 0 or not doconv:
            r += line + '\n'
            continue
        if line[0] != '#': r += line
        else:
            res = 0
            for i in range(7):
                if line[i] != '#':
                    res = i
                    break
            r += line[:res] + ' ' + line[res:]
        r += '\n'
    return r

def cvtarticle(cfg, src, dst, category, title):
    print('{cat}/{art}.html'.format(cat=category, art=title))
    # print(cfg['document'])
    with open(dst, 'w', encoding='utf-8') as fout:
        # fout.write(cfg['document'].format(
        #     name=cfg['name'],
        #     title=title,
        #     category=category,
        #     md=prep(open(src, encoding='utf-8').read())
        # ))
        fout.write(cfg['document']
            .replace('{name}', cfg['name'])
            .replace('{title}', title)
            .replace('{category}', category)
            .replace('{md}', prep(open(src, encoding='utf-8').read()))
        )

def makecatindex(wd, cfg, category, articles):
    print('{cat}/index.html'.format(cat=category))
    with open(wd / 'site' / category / 'index.html', 'w', encoding='utf-8') as f:
        f.write(cfg['category']#.format(
            # name=cfg['name'],
            # category=category,
            # articles='\n'.join([
            #     '<li><a href="{art}.html">{art}</a></li>'.format(
            #         art=article
            #     ) for article in articles
            # ])
            .replace('{name}', cfg['name'])
            .replace('{category}', category)
            .replace('{articles}', '\n'.join([
                '<li><a href="{art}.html">{art}</a></li>'.format(
                    art=article
                ) for article in articles
            ])
        ))

def makeindex(wd, cfg, jobs, index):
    print('index.html')
    index.sort(key=lambda ent: (wd / 'docs' / (ent + '.md')).stat().st_mtime, reverse=True)
    with open(wd / 'site' / 'index.html', 'w', encoding='utf-8') as f:
        f.write(cfg['home']#.format(
            # name=cfg['name'],
            # categories='\n'.join(
            #     '<li><a href="{cat}/">{cat}</a></li>'.format(
            #         cat=category
            #     ) for category in jobs.keys()
            # ),
            # articles='\n'.join(
            #     '<li><a href="{ent}.html">{art} ({cat})</a></li>'.format(
            #         ent=entry, art=entry.split('/')[-1], cat=entry.split('/')[-2]
            #     ) for entry in index
            # )
            .replace('{name}', cfg['name'])
            .replace('{categories}', '\n'.join(
                '<li><a href="{cat}/">{cat}</a></li>'.format(
                    cat=category
                ) for category in jobs.keys()
            ))
            .replace('{articles}', '\n'.join(
                '<li><a href="{ent}.html">{art} ({cat})</a></li>'.format(
                    ent=entry, art=entry.split('/')[-1], cat=entry.split('/')[-2]
                ) for entry in index
            ))
        )

def generate(wd, jobs):
    # print(jobs)
    cfg = readcfg(wd / 'config')
    site = wd / 'site'
    site.mkdir(parents=True, exist_ok=True)
    index = []
    for category in jobs:
        articles = jobs[category]
        # print(category)
        cwd = site / category
        cwd.mkdir(parents=True, exist_ok=True)
        for article in articles:
            cvtarticle(cfg, wd / 'docs' / category / (article + '.md'), wd / 'site' / category / (article + '.html'), category, article)
        makecatindex(wd, cfg, category, articles)
        index += [category + '/' + article for article in articles]
    makeindex(wd, cfg, jobs, index)
    shutil.copytree(wd / 'static', wd / 'site' / 'static', dirs_exist_ok=True)

def main():
    try:
        wd = Path(sys.argv[1])
    except:
        wd = Path(input('Drag blog folder: '))
    jobs = grabjobs(wd / 'docs')
    generate(wd, jobs)
    
if __name__ == '__main__':
    main()
