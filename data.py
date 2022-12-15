import csv

class Task():
    def __init__(self, type, full_type, subtype, variant, solution_method, num_of_solutions, file_name,svg):
        self.type = type
        self.full_type = full_type
        self.subtype = subtype
        self.variant = variant
        self.solution_method = solution_method
        self.num_of_solutions = num_of_solutions
        self.file_name = file_name
        self.svg = svg

tasks = {}
with open("src/tasks_data.csv", mode="r", encoding="utf-8") as data_file:
    csv_reader = csv.reader(data_file, delimiter=";")
    linecount = 0

    for row in csv_reader:
        linecount += 1
        if linecount == 1:
            header = row
            continue
        elif linecount == 2:
            continue
        type = "".join(sorted(row[0].lower()))
        full_type = type.replace("b", "BOD ").replace("k", "KRUŽNICE ").replace("p", "PŘÍMKA ").rstrip().replace(" ", " 🞄 ")
        subtype = row[1]
        variant = row[2]
        solution_method = row[3]
        num_of_solutions = row[4]
        file_name = row[5]
        svg = row[6]
        new_task = Task(type, full_type, subtype, variant, solution_method, num_of_solutions, file_name,svg)
        tasks[type] = tasks.get(type, []) + [new_task]