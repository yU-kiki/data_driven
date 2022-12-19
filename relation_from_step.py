# データドリブン課題10
# 歩数計から得られるログで人間関係を推測する

import csv

groups = ['A', 'B', 'C']
numbers = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
filenames_a = []
filenames_all = []
output = []

for group in range(len(groups)):
    for number in range(len(numbers)):
        filename = f'{groups[group]}_{numbers[number]}'
        if group == 0:
            filenames_a.append(filename)
        filenames_all.append(filename)

# 課題３
filenames = filenames_a
output_file_name = 'output_group_a.csv'

# 課題４
# filenames = filenames_all
# output_file_name = 'output_group_all.csv'

for name_a in filenames:
    output_rows = []
    for name_b in filenames:
        if name_a == name_b:
            output_rows.append('-')
        else:
            filename_a = f'./data_sfc/{name_a}.csv'
            filename_b = f'./data_sfc/{name_b}.csv'

            data_a = []
            data_b = []
            data_num = 60 * 24 * 15

            with open(filename_a, encoding='utf8', newline='') as f:
                csvreader = csv.reader(f)
                for row in csvreader:
                    if not row[2] == 'steps':
                        data_a.append(int(row[2]))
            with open(filename_b, encoding='utf8', newline='') as f:
                csvreader = csv.reader(f)
                for row in csvreader:
                    if not row[2] == 'steps':
                        data_b.append(int(row[2]))

            step_diffs = []
            standards = []

            for i in range(data_num):
                stepDiff = (data_a[i] - data_b[i]) ** 2
                normalize = data_a[i] ** 2 + data_b[i] ** 2
                step_diffs.append(stepDiff)
                standards.append(normalize)

            top = 0
            bottom = 0
            d = 0
            continue_count = 0
            point = 0

            for i in range(data_num - 59):
                top = sum(step_diffs[i: i + 60])
                bottom = sum(standards[i: i + 60])
                if bottom >= 5500:
                    d = top / bottom
                    if d <= 0.05:
                        continue_count += 1
                        if continue_count >= 15:
                            point += 1 
                    else:
                        continue_count = 0

            output_rows.append(point)

    output.append(output_rows)


with open(output_file_name, 'w') as f:
    writer = csv.writer(f)
    writer.writerow([''] + filenames)
    for i, row in zip(filenames, output):
        writer.writerow([i] + row)

with open(output_file_name) as f:
    print(f.read())