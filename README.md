# Introduction  

Aims at [MEITU131](https://www.meitu131.net).  

# Specification  

> Built on `macOS 13.1`  
> with os built-in `Python: 3.9.6`  
> utilising `scrapy` `pillow` `pandas`  
> as well as `playwright` for JS-loaded elements  

# Contents

Contains one scrapy projects (for now):  
- `meitu` starting with the page [女神大全](https://www.meitu131.net/nvshen/), it collects the entire girls including those invisible ones in the index page, sorts them according to the "Score" (JS-loaded element in each model's page), and parses the selected ones.
