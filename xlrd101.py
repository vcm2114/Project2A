from xlrd import open_workbook
# Exemple de base
xls=open_workbook('data.xls')
list1=[]
for col in range(xls.sheets()[1].ncols):
   for rows in range(xls.sheets()[1].nrows):
      list1.append(str(xls.sheets()[1].cell(rows, col).value))
print(list1)

# To run a script in python command line:
# >>> exec(open("excel.py").read(), globals())

def import_xls(path,n,m):
   xl=open_workbook(path)
   movies=[]
   names=[]
   for col in range(xl.sheets()[1].ncols):
      for rows in range( min(xl.sheets()[1].nrows,m) ):
         movies.append(str(xl.sheets()[1].cell(rows, col).value))
   for col in range(xl.sheets()[2].ncols):
      for rows in range( min(xl.sheets()[2].nrows,n) ):
         names.append(str(xl.sheets()[2].cell(rows, col).value))
   return [names,movies]

[e,r] = import_xls('data.xls',5,3)
print(e)
