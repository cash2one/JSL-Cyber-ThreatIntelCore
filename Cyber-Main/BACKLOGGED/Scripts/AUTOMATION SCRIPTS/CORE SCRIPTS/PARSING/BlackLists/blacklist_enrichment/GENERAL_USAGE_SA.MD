#How to use Scrapy scripts

##What are spiders?

- Spiders are the main script defining crawling and scraping activity

##The Scrapy directory

project_name/
    scrapy.cfg            # deploy configuration file

    project_name/             # project's Python module, you import your code
        __init__.py

        items.py          # project items file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you put your spiders
            __init__.py
            ...


##General instructions for scripts contained in the "blacklist_enrichment" Scrapy project

##Where to find the spiders

- All spiders (Scrapy scraping scripts) in the "blacklist_enrichment" project, can be found in the following directory on GitHub:
	- cyber\CORE SCRIPTS\PARSING\BlackLists\blacklist_enrichment\spiders

- On your local repository, they will be located as follows:
	- your_path_to_JSL_local_repository\cyber\CORE SCRIPTS\PARSING\BlackLists\blacklist_enrichment


##Working with Scrapy

- Working in the shell
	- Open up the command prompt
	- cd into the appropriate directory, for example: Your_path_to_JSL_local_repository\cyber\CORE SCRIPTS\PARSING\BlackLists\blacklist_enrichment
	- enter the following command, replacing "data_source_url" with relevant URL
		- scrapy shell "data_source_url"
	- The shell is an invaluable tool for testing xpaths, regular expressions and so on, and, in general, the output


- How to run a spider
	- open up command prompt
	- cd into a directory such as the following: 
	Your_path_to_JSL_local_repository\cyber\CORE SCRIPTS\PARSING\BlackLists\blacklist_enrichment
	- enter for example: scrapy crawl "spider_name"

- How to run a spider and write data to CSV file
	- open up command prompt
	- cd into a directory such as the following: 
	Your_path_to_JSL_local_repository\cyber\CORE SCRIPTS\PARSING\BlackLists\blacklist_enrichment
	- enter for example: scrapy crawl "spider_name" -o spider_output.csv
