import csv
import unicodedata

class Task():
    def __init__(self, type, subtype, variant, solution_method, num_of_solutions, file_name,svg):
        self.type = type
        self.subtype = subtype
        self.variant = variant
        self.solution_method = solution_method
        self.num_of_solutions = num_of_solutions
        self.file_name = file_name
        self.svg = svg

    def get_path_name_cs(self):
        # replace accent characters
        path = unicodedata.normalize('NFD', self.variant).encode('ascii', 'ignore').decode("utf-8")
        # replace unwanted characters
        chars_to_remove = [",", ".", ";", "-", "_", "/", "\\"]
        for char in chars_to_remove:
            path = path.replace(char, "")
        # replace spaces
        path = path.replace(" ", "-")
        path = path.lower()
        return path

    def get_full_type_cs(self):
        return self.type.replace("B", "BOD ").replace("K", "KRUŽNICE ").replace("P", "PŘÍMKA ").rstrip().replace(" ", " 🞄 ")


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
        type = "".join(sorted(row[0].upper()))
        subtype = row[1]
        variant = row[2][0].upper() + row[2][1:].lower()
        solution_method = row[3]
        num_of_solutions = row[4]
        file_name = row[5]
        svg = row[6]
        new_task = Task(type, subtype, variant, solution_method, num_of_solutions, file_name,svg)
        tasks[type] = tasks.get(type, []) + [new_task]