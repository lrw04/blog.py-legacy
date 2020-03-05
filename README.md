# blog.py
A static blog generator.

## Usage
Download `blog.py` from repository. Run `blog.py`. Drag folder with files to the terminal window and press enter.
Resulting site will be in `site` of the directory.

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
static/                 - Static files, will be present in ../static
```

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
