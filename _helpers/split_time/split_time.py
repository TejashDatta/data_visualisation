import csv

csv_read_file = open('delhi_air.csv', 'r')
csv_output_file = open('out.csv', 'w')
csv_reader = csv.reader(csv_read_file)
csv_writer = csv.writer(csv_output_file)


for row in csv_reader:
    wrow = [row[0][:4], row[0][4:6], row[0][6:8], row[0][9:]] + row[1:]
    csv_writer.writerow(wrow)

csv_output_file.close()
csv_read_file.close()