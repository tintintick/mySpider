import csv

class CsvOutPuter(object):
    def outputtocsv(self, data, filename):
        fobj = file(filename, "a")
        writer = csv.writer(fobj)
        writer.writerow(data)
        fobj.close()