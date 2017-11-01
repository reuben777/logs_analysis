#!/usr/bin/env python3
import psycopg2
import datetime

global report_file


def init(filename=''):
    global report_file
    if len(filename) > 0:
        # Clean reporting file
        open('reports/' + filename + '.txt', 'w').close()
        # specified reporting_file
        report_file = open(filename + '.txt', 'w')
    else:
        # Date based reporting file
        t = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")
        report_file = open('reports/' + t + '_report' + '.txt', 'w')
        writePrintStr("Report Generated on: {} \n".format(t))
    # upchuckArticleViews()
    # upchuckAuthorViews
    upchuckErrorDays()
    report_file.close()


def getConnectionToDb():
    return psycopg2.connect("dbname=news")


def fetchAll(sql=''):
    db = getConnectionToDb()
    c = db.cursor()
    c.execute(sql)
    results = c.fetchall()
    db.close()
    return results


def writePrintStr(question=''):
    global report_file
    print(question + '\n')
    report_file.write(question)


def upchuckArticleViews():
    writePrintStr('What are the most popular three articles of all time?')
    articles = fetchAll('''
    SELECT title, popularity
        from article_log
        order by popularity DESC
        limit 3
    ''')
    for article in articles:
        str_views = str(int(article[1]))
        file_line = '  "{}"" - {} views\n'.format(article[0], str_views)
        writePrintStr(file_line)


def upchuckAuthorViews():
    writePrintStr('Who are the most popular article authors of all time?')
    authors = fetchAll('''
    SELECT a.name, sum(al.popularity) as author_popularity
    FROM article_log as al
    LEFT JOIN authors as a ON al.author_id = a.id
    GROUP BY (al.author_id, a.name)
    ORDER BY author_popularity DESC
    ''')
    for author in authors:
        str_views = str(int(author[1]))
        file_line = '  {} - {} views\n'.format(author[0], str_views)
        writePrintStr(file_line)


# WHERE l.status != '200 OK'
def upchuckErrorDays():
    writePrintStr('On which days did more than 1% of requests lead to errors?')
    error_days = fetchAll('''
    SELECT
    lok.status,
    lforofor.status as error,
    date_trunc('day', lok.time) as day,
    count(lok.id) as occurences
    FROM log AS lok
        RIGHT JOIN (
            SELECT
            logg.status,
            date_trunc('day', logg.time) as errorday,
            count(logg.id) as occurences
            FROM log AS logg
            WHERE logg.status NOT LIKE CONCAT('%','200 OK', '%')
            GROUP BY (logg.status, day)
            LIMIT 20
            ) as lforofor
        ON day = errorday
    GROUP BY (lok.status, day, error)
    LIMIT 20;
    ''')
    # print(error_days)
    for error in error_days:
        print("status: {}, error: {}, day: {}, count: {}".format(
            error[0], error[1], error[2], error[3]))


init()
