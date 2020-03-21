# blog.py
A static blog generator.

## Usage
 1. Download `blog.py` from repository. Run `blog.py`. Drag folder with files to the terminal window and press enter.
Resulting site will be in `site` of the directory.

 1. Copy `blog.py` and `new.py` to blog directory, compile by running `blog.py` and adding entries by running `new.py`.

Depends on `pandoc`.

### Folder configuration
```
config/
  category.html         - Template for index of category
  ci.html               - Template for entries of categories
  cii.html              - Template for entries of articles on the category page
  document.html         - Template for one article
  home.html             - Template for home page
  ii.html               - Template for entries of articles on home page
  name.txt              - Title of blog
docs/
  <categories>/
    <articles>.md
    <articles>.txt      - Timestamp of article, can be in any format
static/                 - Static files, will be present in ../static
```

#### Timestamping
Articles are expected to be timestamped in a `.txt` file with the same name.

The default format used in `new.py` is `priority(2) year(4) month(2) day(2)`.

### Templating
#### `category.html`
 - `{name}`: content of `config/name.txt`, stripped;
 - `{category}`: name of category;
 - `{articles}`: list of links to articles under this category (should be in `<ul>...</ul>`).
 
#### `document.html`
 - `{name}`: content of `config/name.txt`, stripped;
 - `{category}`: name of category;
 - `{title}`: title of article;
 - `{html}`: HTML compiled from Markdown.
 
#### `home.html`
 - `{name}`: content of `config/name.txt`, stripped;
 - `{categories}`: list of links to category indexes;
 - `{articles}`: list of links to articles.

#### `ci.html`
 - `{cat}`: name of category.

#### `cii.html`
 - `{art}`: name of article.

#### `ii.html`
 - `{art}`: name of article;
 - `{cat}`: name of category.
