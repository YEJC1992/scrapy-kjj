import csv

    
def createCsv(filename,header):
    f = open(filename,'w',encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    f.close()