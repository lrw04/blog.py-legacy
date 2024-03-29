import subprocess
import shutil
import sys
import os
from pathlib import Path


def m(s): return s + '.md'


def h(s): return s + '.html'


def t(s): return s + '.txt'


def search(dir: Path) -> dict:
    jobs = {}
    for category in dir.iterdir():
        if not category.is_dir():
            continue
        jobs[category.name] = []
        for article in category.iterdir():
            if article.suffix == '.md':
                jobs[category.name].append(article.name[:-3])
    return jobs


def readcfg(cdir: Path) -> dict:
    return {
        'home': open(cdir / 'home.html', encoding='utf-8').read(),
        'cat': open(cdir / 'category.html', encoding='utf-8').read(),
        'doc': open(cdir / 'document.html', encoding='utf-8').read(),
        'name': open(cdir / 'name.txt', encoding='utf-8').read().strip(),
        'cii': open(cdir / 'cii.html', encoding='utf-8').read(),
        'ii': open(cdir / 'ii.html', encoding='utf-8').read(),
        'ci': open(cdir / 'ci.html', encoding='utf-8').read()
    }


def mkart(cfg: dict, wd: Path, cat: str, art: str, jobs: dict):
    print(cat, art)

    subprocess.run([
        'pandoc', str(wd / 'docs' / cat / m(art)), '--katex',
        '--no-highlight', '-o', str(wd / 'tmp' / 'tmp.html')
    ])
    print(' '.join([
        'pandoc', str(wd / 'docs' / cat / m(art)), '--katex',
        '--no-highlight', '-o', str(wd / 'tmp' / 'tmp.html')
    ]))

    frag = open(wd / 'tmp' / 'tmp.html', encoding='utf-8').read()
    with open(wd / 'site' / cat / h(art), 'w', encoding='utf-8') as fout:
        fout.write(cfg['doc']
                   .replace('{name}', cfg['name'])
                   .replace('{title}', art)
                   .replace('{category}', cat)
                   .replace('{html}', frag)
                   .replace('{categories}', '\n'.join([
                       cfg['ci'].replace('{cat}', cat) for cat in sorted(jobs.keys())]))
                   )


def mkcat(cfg: dict, wd: Path, cat: str, arts: list, jobs: dict):
    print(cat)
    with open(wd / 'site' / cat / 'index.html', 'w', encoding='utf-8') as fout:
        fout.write(cfg['cat']
                   .replace('{name}', cfg['name'])
                   .replace('{articles}', '\n'.join([
                       cfg['cii'].replace('{art}', art) for art in sorted(arts)
                   ]))
                   .replace('{category}', cat)
                   .replace('{categories}', '\n'.join([
                       cfg['ci'].replace('{cat}', cat) for cat in sorted(jobs.keys())]))
                   )


def gettime(ent: tuple):
    return open(ent[2] / 'docs' / ent[0] / t(ent[1]), encoding='utf-8').read().strip()


def mkindex(cfg: dict, wd: Path, jobs: dict):
    print('/')
    entries = []
    for category in jobs:
        for article in jobs[category]:
            entries.append((category, article, wd))
    entries.sort(key=gettime, reverse=True)
    with open(wd / 'site' / 'index.html', 'w', encoding='utf-8') as fout:
        fout.write(cfg['home']
                   .replace('{name}', cfg['name'])
                   .replace('{categories}', '\n'.join([
                       cfg['ci'].replace('{cat}', cat) for cat in sorted(jobs.keys())]))
                   .replace('{articles}', '\n'.join([
                       cfg['ii'].replace('{cat}', cat).replace('{art}', art)
                       for cat, art, _ in entries
                   ]))
                   )


def gen(wd: Path):
    jobs = search(wd / 'docs')
    cfg = readcfg(wd / 'config')
    shutil.rmtree(wd / 'site', ignore_errors=True)
    (wd / 'site').mkdir(parents=True, exist_ok=True)
    (wd / 'tmp').mkdir(parents=True, exist_ok=True)
    for category in jobs:
        articles = jobs[category]
        (wd / 'site' / category).mkdir(parents=True, exist_ok=True)
        for article in articles:
            mkart(cfg, wd, category, article, jobs)
        mkcat(cfg, wd, category, articles, jobs)
    mkindex(cfg, wd, jobs)
    try: shutil.rmtree(wd / 'site' / 'static')
    except: pass
    shutil.copytree(wd / 'static', wd / 'site' / 'static')
    shutil.rmtree(wd / 'tmp')


def main():
    try:
        wd = Path(sys.argv[1])
    except IndexError:
        if Path('./docs').exists():
            wd = Path('.')
        else:
            wd = Path(input('Blog directory: ').strip())
    gen(wd)


if __name__ == '__main__':
    main()
