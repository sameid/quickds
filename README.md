# quickds - Automate Datasource Creation via the Klipfolio API #

quickds will parse a CSV file with a list of datasource configurations.
Then it will create them on the environment you point to via the configuration
block.

## Getting Started ##

First thing to do is configure the script using the config.json file.

config.json
``` javascript
{
	"host": "https://test-app.klipfolio.com/api/1",	//environment where datasources will be created
	"user": "ab+klipfolio@klipfolio.com", //username 
	"pass": "ihaveallthekeys", //password
	"input": "input.csv", //datasource configuration file
}
```

Ensure your datasource configuration file has the datasource creation information that you want.
- Remember that columns 1 .. 5 (name, format, refresh, oauth, query) are manditory and must maintain order.
- Columns 6 .. * can be dynamic and must relate to parameters in the "query" column to make any changes to the "query"

input.csv (can be named anything, so long as you specify it in the config.json file)
```
name,format,refresh,oauth,query,ids,dimension,metrics,filters,start-date,end-date,max-results
ds1,csv,300,bee05039efe0bb0f0bb007afcc116f94,https://www.googleapis.com/analytics/v3/data/ga?ids=*&dimensions=*&metrics=*&filters=*&start-date=*&end-date=*&max-results=*,ga:47757403,ga:visitors,ga:avgTimeOnPage,ga:country==Russia,{date.startOfYear},{date.today},10000
ds2,csv,300,bee05039efe0bb0f0bb007afcc116f94,https://www.googleapis.com/analytics/v3/data/ga?ids=*&dimensions=*&metrics=*&filters=*&start-date=*&end-date=*&max-results=*,ga:47757403,ga:visitors,ga:avgTimeOnPage,ga:country==Russia,{date.startOfYear},{date.today},10000
```

#### Running the script ####

Once you have configured everything. Run the script:

```
$ python quickds.py
```

Optionally tell it what file to use on the fly:

```
$ python quickds.py my_ds_file.csv
```

## Quirks ##

- Currently the API doesn't expose anything for OAuth tokens. What this means is that when you specify the publicId of the OAuth token in the input.csv file,
it won't actually use that token, and most likely the report on the creation of that datasource will show an error. For now just specify a publicId of
a datasource that is using an OAuth token that you want. (Adding OAuth token API support is on the roadmap)
