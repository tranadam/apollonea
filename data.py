import csv
import unicodedata

class Task():
    def __init__(self, type, subtype_cs, subtype_en, variant_cs, variant_en, solution_method_cs, solution_method_en, num_of_solutions, file_name,svg):
        self.type = type
        self.subtype_cs = subtype_cs
        self.subtype_en = subtype_en
        self.variant_cs = variant_cs
        self.variant_en = variant_en
        self.solution_method_cs = solution_method_cs
        self.solution_method_en = solution_method_en
        self.num_of_solutions = num_of_solutions
        self.file_name = file_name
        self.svg = svg

    def get_type(self, lang):
        if lang == "cs":
            return self.type
        elif lang == "en":
            return self.type.replace("p", "l").replace("k", "c").replace("b", "p")

    def get_variant(self, lang):
        if lang == "cs":
            return self.variant_cs
        elif lang == "en":
            return self.variant_en

    def get_solution_method(self, lang):
        if lang == "cs":
            return self.solution_method_cs
        elif lang =="en":
            return self.solution_method_en

    def get_path_name(self, lang):
        variant = self.get_variant(lang)

        # replace accent characters
        path = unicodedata.normalize('NFD', variant).encode('ascii', 'ignore').decode("utf-8")
        # replace unwanted characters
        chars_to_remove = [",", ".", ";", "-", "_", "/", "\\"]
        for char in chars_to_remove:
            path = path.replace(char, "")
        # replace spaces
        path = path.replace(" ", "-")
        path = path.lower()
        return path

    def get_full_type(self, lang):
        if lang == "cs":
            return self.type.replace("b", "BOD ").replace("k", "KRUŽNICE ").replace("p", "PŘÍMKA ").rstrip().replace(" ", " 🞄 ")
        elif lang =="en":
            return self.type.replace("b", "POINT ").replace("k", "CIRCLE ").replace("p", "LINE ").rstrip().replace(" ", " 🞄 ")

    def get_text_file_name(self, lang):
        if lang == "cs":
            return self.file_name + ".txt"
        elif lang == "en":
            return self.file_name + "_en.txt"


class Tasks():
    def __init__(self, tasks_dictionary):
        self.tasks = tasks_dictionary

    def get_same_type_tasks(self, compared_task, lang):
        same_type_tasks = self.tasks[compared_task.type.lower()]
        result_data = []
        for task in same_type_tasks:
            if task == compared_task:
                continue
            result_data.append({"task_name": task.get_variant(lang), "task_path": task.get_path_name(lang)})
        return result_data

tasks_dict = {}
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
        subtype_cs = row[1]
        subtype_en = row[2]
        variant_cs = row[3][0].upper() + row[3][1:].lower()
        variant_en = row[4][0].upper() + row[4][1:].lower()
        solution_method_cs = row[5]
        solution_method_en = row[6]
        num_of_solutions = row[7]
        file_name = row[8]
        svg = row[9]
        new_task = Task(type, subtype_cs, subtype_en, variant_cs, variant_en, solution_method_cs, solution_method_en, num_of_solutions, file_name, svg)
        tasks_dict[type] = tasks_dict.get(type, []) + [new_task]

tasks = Tasks(tasks_dict)