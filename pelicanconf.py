AUTHOR = 'hugu'
SITENAME = 'digtalsheep'
SITEURL = 'https://cj233cj.github.io/'
SITETITLE = "project digtalsheep"
SITEDESCRIPTION = "the dream"
SITELOGO = SITEURL + "/images/profile.jpg"
FAVICON = SITEURL + "/images/favicon.ico"
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'en'


PATH = 'content'
THEME = 'themes/Papyrus'
THEME_STATIC_PATHS = ['static']
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['readtime', 'neighbors']
#PLUGINS = ['readtime', 'search', 'neighbors', 'pelican-toc']

DISPLAY_PAGES_ON_MENU = True
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives',))
#DIRECT_TEMPLATES = (('index', 'search', 'tags', 'categories', 'archives',))
PAGINATED_TEMPLATES = {'index':None,'tag':None,'category':None,'author':None,'archives':24,}

# Site search plugin
#SEARCH_MODE = "output"
#SEARCH_HTML_SELECTOR = "main"
# Table of Content Plugin
TOC = {
    'TOC_HEADERS'       : '^h[1-3]', # What headers should be included in
                                     # the generated toc
                                     # Expected format is a regular expression
    'TOC_RUN'           : 'false',    # Default value for toc generation,
                                     # if it does not evaluate
                                     # to 'true' no toc will be generated
    'TOC_INCLUDE_TITLE': 'false',    # If 'true' include title in toc
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
RSS_FEED_SUMMARY_ONLY = True

# Social widgets
SOCIAL = (
    ('github', ''),
    ('twitter', ':)'),
)

# Article share widgets
SHARE = (
    ("twitter", "https://twitter.com/intent/tweet/?text=Features&amp;url="),
   
    ("reddit", "https://reddit.com/submit?url="),

    ("telegram", "https://telegram.me/share/url?text=Features&amp;url="),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# DISQUS_SITENAME = ''
# GOOGLE_ANALYTICS = ''
