# Logs Analysis Project

My own udacity project for analysing a projects data and reporting on my various findings.

You can find the rubric [here](https://review.udacity.com/#!/rubrics/277/view)

## Getting Started
### Gettings the data
Download the `newsdata.sql` database [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Once downloaded, move to inside `/logs_analysis/vagrant`
### Installation
1. Install
```
$ cd /{user_path_to_project}/logs_analysis/vagrant
$ vagrant up
```
2. Login with vagrant guest user `$ vagrant ssh`

3. Change directory to vagrant shared files: `cd /vagrant`

4. Load the data in: `@vagrant$ psql -d news -f newsdata.sql`

5. Now run the python program `@vagrant$ python newsdata.py`

## License
Licensed under the [MIT License](https://github.com/reuben777/logs_analysis/LICENSE.md)
