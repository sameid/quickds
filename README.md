# quickds - Automate Datasource Creation via the Klipfolio API #

quickds will parse a CSV file with a list of datasource configurations.
Then it will create them on the environment you point to via the configuration
block.

## Getting Started ##

First thing to do is configure the script using the config.json file.

```
{
	"host": "https://test-app.klipfolio.com/api/1",	//environment where datasources will be created
	"user": "ab+klipfolio@klipfolio.com", //username 
	"pass": "ihaveallthekeys", //password
	"input": "input.csv" //datasource configuration file
}
```


| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
