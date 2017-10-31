# Logs Analysis Project

My own udacity project for analysing a projects data and reporting on my various findings.

You can find the rubric [here](https://review.udacity.com/#!/rubrics/277/view)

## Getting Started

### Virtual Environment

You can gollow the [Udacity Setup Guide](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0) if you have access to this specific lesson.

**or**

1. Download the tools [Vagrant](https://www.vagrantup.com/downloads.html) and [Virtualbox v5.1](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
> We use Virtualbox v5.1 library because of conflicts that arise between newer Virtualbox versions and the python library we use for the VM.

2. Install both (you may need to restart your system)

### The Data
Download the `newsdata.sql` database [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Once downloaded, move to inside `/logs_analysis/vagrant/`

### Installation
1. Install
```
$ cd /{user_path_to_project}/logs_analysis/vagrant
$ vagrant up
```
> Note: This may take some time.

2. Login with vagrant guest user `$ vagrant ssh`

3. Change directory to vagrant shared files: `cd /vagrant`

4. Load the data in: `@vagrant$ psql -d news -f newsdata.sql`
   - `psql` — the PostgreSQL command line program
   - `-d news` — connect to the database named news which has been set up for you
   - `-f newsdata.sql` — run the SQL statements in the file _newsdata.sql_

5. Same for `newsdata_custom.sql`
   - `@vagrant$ psql -d news -f newsdata_custom.sql`

6. Now run the python program `@vagrant$ python newsdata_custom.sql`

## API

## DB Overview

### Language
Postgresql

### Tables:
* _articles_

Column | Type | Modifiers
:---:|:---:|:---:
author | integer | not `null`
title  | *text* | not `null`
slug   | *text* | not `null`
lead   | *text* |
body   | *text* |
time   | *timestamp* with time zone | default `now()`
id     | *integer* | not `null` default `nextval('articles_id_seq'::regclass)`

* _authors_

Column | Type | Modifiers
:--:|:---:|:---:
name | *text* | not `null`
bio | *text* |
id | *integer* | not `null` default `nextval('authors_id_seq'::regclass)`

* _log_

Column | Type | Modifiers
:---:|:---:|:---:
path | *text* |
ip | *inet* |
method | *text* |
status | *text* |
time | *timestamp* with time zone | default `now()`
id | *integer* | not `null` default `nextval('log_id_seq'::regclass)`

## License
Licensed under the [MIT License](https://github.com/reuben777/logs_analysis/LICENSE.md)
