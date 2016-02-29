from xlrd import open_workbook

# To run a script in python command line:
# >>> exec(open("excel.py").read(), globals())

def import_xls(path,n,m):
   xl=open_workbook(path)
   movies=[]
   names=[]
   for rows in range( min(xl.sheets()[1].nrows,m) ):
      movies.append(str(xl.sheets()[1].cell(rows, 0).value))
   for rows in range( min(xl.sheets()[2].nrows,n) ):
      names.append(str(xl.sheets()[2].cell(rows, 0).value))
   return [names,movies]

[e,r] = import_xls('data.xls',5,3)
print(e)
