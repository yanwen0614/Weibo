def Create_insert_sql(tablename, *arg):
    sql = tablename.join(('''INSERT INTO ''',''' ({})  VALUES  ({})'''))
    attr = ','.join(arg)
    placeholder  = ','.join(["'{}'" for _ in range(len(arg))])
    sql = sql.format(attr,placeholder)
    return sql


def Create_createtable_sql(tablename,Key, **kwarg):
    sql = "CREATE TABLE `{tablename}` (placeholderplaceholder,\
    PRIMARY KEY (`{Key}`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;".format(tablename=tablename,Key=Key)
    attr = []
    for k, w in kwarg.items():
        attr.append("`{k}` {w} ".format(k=k,w=w))
    return ','.join(attr).join(sql.split('placeholderplaceholder'))
