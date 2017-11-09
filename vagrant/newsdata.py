#!/usr/bin/env python3
import psycopg2
from datetime import datetime
from decimal import Decimal, ROUND_DOWN

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
        t = datetime.now().strftime("%y_%m_%d_%H_%M_%S")
        report_file = open('reports/' + t + '_report' + '.txt', 'w')
        writePrintStr("Report Generated on: {} \n".format(t))
    upchuckArticleViews()
    upchuckAuthorViews()
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
    writePrintStr('What are the most popular three articles of all time?\n')
    articles = fetchAll('''
    SELECT title, popularity
        from article_log
        order by popularity DESC
        limit 3;
    ''')
    for article in articles:
        str_views = str(int(article[1]))
        file_line = '  "{}" - {} views\n'.format(article[0], str_views)
        writePrintStr(file_line)


def upchuckAuthorViews():
    writePrintStr('Who are the most popular article authors of all time?\n')
    authors = fetchAll('''
    SELECT a.name, sum(al.popularity) as author_popularity
    FROM article_log as al
    LEFT JOIN authors as a ON al.author_id = a.id
    GROUP BY (al.author_id, a.name)
    ORDER BY author_popularity DESC;
    ''')
    for author in authors:
        str_views = str(int(author[1]))
        file_line = '  {} - {} views\n'.format(author[0], str_views)
        writePrintStr(file_line)


# WHERE l.status != '200 OK'
def upchuckErrorDays():
    writePrintStr(
        'On which days did more than 1% of requests lead to errors?\n')
    error_days = fetchAll('''
    SELECT subq.day, subq.perc from log as log_info
    RIGHT JOIN
    (SELECT
        lgood.goodday as day,
        lgood.goodoccurences as goodcount,
        (count(*)::decimal / lgood.goodoccurences::decimal)*100 as perc,
        count(*) as occurences
        FROM log AS lbad
            RIGHT JOIN (
                SELECT
                date_trunc('day', logg.time) as goodday,
                count(*) as goodoccurences
                FROM log AS logg
                WHERE logg.status LIKE CONCAT('%','200 OK', '%')
                GROUP BY 1
                LIMIT 20
            ) as lgood
            ON date_trunc('day', lbad.time) = lgood.goodday
    WHERE lbad.status NOT LIKE CONCAT('%','200 OK', '%')
    GROUP BY 1,2)
    as subq
    ON date_trunc('day', log_info.time) = subq.day
    WHERE subq.perc > 1
    GROUP BY 1,2;
    ''')

    for error in error_days:
        perc = Decimal(error[1]).quantize(
            Decimal('.1'), rounding=ROUND_DOWN)
        day = datetime.strftime(error[0], '%B %d, %Y')
        file_line = "  {} - {}% errors\n".format(
            day, perc)
        writePrintStr(file_line)


init()
