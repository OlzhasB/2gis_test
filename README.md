# 2gis_test
This console app allows you to parse large xml_files with people and their work schedule
and calculate time spent at work


#### Command to run
This command builds new image according to info in Dockerfile
and removes it after script completion 
```
docker-compose run --rm console_app
```

#### data
```
'people.xml' is an xml file with correct format,
you can write the path to this file 'data/people.xml'
in console dialogue with script to parse it
```

```
'wrong.xml' is an xml file with invalid format for tests
```