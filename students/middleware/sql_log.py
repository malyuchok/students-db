# -*- coding: utf-8 -*-
import os
import time
import datetime

from django.conf import settings
from django.db import connection
from django.template import Template, Context


class SQLLogMiddleware:
    def process_request(self, request):
        request.sql_log_start = time.time()

    def process_response(self, request, response):
        # request.sqllog_start is empty if an append slash redirect happened.
        debug_sql = getattr(settings, "DEBUG_SQL", False)
        if (not request.sql_log_start) or not (settings.DEBUG and debug_sql):
            return response

        timesql = 0.0
        for q in connection.queries:
            timesql += float(q['time'])
        seen = {}
        duplicate = 0
        for q in connection.queries:
            sql = q["sql"]
            c = seen.get(sql, 0)
            if c:
                duplicate += 1
            if c:
                q["seen"] = c + 1
            seen[sql] = c + 1

        t = Template('''
            <div class="container">
                <div class="sql_time">
                <table class="table table-hover table-striped">
                    <tr>
                      <th>request.path:</th>
                      <th>Total query count </br> (Загальна кількість запитів)</th>
                      <th>Total duplicate query count </br> (Загальна кількість дублікатів запитів)</th>
                      <th>Total SQL execution time </br> (Загальний час виконання SQL)</th>
                      <th>Total Request execution time </br> (Загальний час виконання запиту)</th>
                    </tr>
                    <tr>
                        <td>{{ request.path|escape }}</td>
                        <td>{{ queries|length }}</td>
                        <td>{{ duplicate }}</td>
                        <td>{{ timesql }}</td>
                        <td>{{ timerequest }}</td>
                    </tr>
                </table>
                </div>
                <table class="table table-hover table-striped">
                 <tr>
                  <th>Time</th>
                  <th>Seen</th>
                  <th>SQL</th>
                 </tr>
                    {% for sql in queries %}
                        <tr>
                         <td>{{ sql.time }}</td>
                         <td align="right">{{ sql.seen }}</td>
                         <td>{{ sql.sql }}</td>
                        </tr>
                    {% endfor %}
                </table>
            </div>
        ''')
        timerequest = round(time.time() - request.sql_log_start, 3)
        queries = connection.queries
        html = t.render(Context(locals()))
        if debug_sql == True:
            if response.get("content-type", "").startswith("text/html"):
                response.write(html)
                del (response['ETag'])
            return response

        assert os.path.isdir(debug_sql), debug_sql
        outfile = os.path.join(debug_sql, "%s.html" % datetime.datetime.now().isoformat())
        fd = open(outfile, "wt")
        html = u'''<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>SQL Log %s</title></head><body><a href="./">Directory</a><br>%s</body></html>''' % (
            request.path, html)
        fd.write(html.encode('utf8'))
        fd.close()
        return response