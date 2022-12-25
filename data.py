import csv
import unicodedata

class Task():
    def __init__(self, type, subtype_cs, subtype_en, variant_cs, variant_en, solution_methods_cs, solution_methods_en, num_of_solutions, svg):
        self.type = type
        self.subtype_cs = subtype_cs
        self.subtype_en = subtype_en
        self.variant_cs = variant_cs
        self.variant_en = variant_en
        self.solution_methods_cs = solution_methods_cs
        self.solution_methods_en = solution_methods_en
        self.num_of_solutions = num_of_solutions
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

    def get_solution_methods(self, lang):
        if lang == "cs":
            return self.solution_methods_cs
        elif lang =="en":
            return self.solution_methods_en

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

    def get_construction_steps(self,file_name):
        path_base = "src/task_data/"
        # text_file_path = path_base + self.type.upper() + "/" + file_name
        text_file_path = "src/task_data/BPP/bpp_ruznobezky_bod_mimo_primky.txt" # correctly formated file as a placeholder
        with open(text_file_path, mode="r", encoding="utf-8") as file_steps:
            pre_steps = file_steps.read()
            pre_steps = pre_steps.split("\n")
            steps = []
            for step in pre_steps:
                if len(step) == 0:
                    continue

                # Set italic parts
                open_tag = True
                while True:
                    if "*" not in step:
                        break
                    if open_tag:
                        step = step.replace("*", "<i>", 1)
                    elif not open_tag:
                        step = step.replace("*", "</i>", 1)
                    open_tag = not open_tag

                steps.append(step[step.index(".")+1:].strip())
        return steps

    def get_same_type_tasks(self, tasks, lang):
        same_type_tasks = tasks[self.type.lower()]
        result_data = []
        for task in same_type_tasks:
            if task == self:
                continue
            result_data.append(task)
        return result_data


def merge_tasks(task1, task2):
    task1.solution_methods_cs.extend(task2.solution_methods_cs)
    task1.solution_methods_en.extend(task2.solution_methods_en)
    return task1


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
        subtype_cs = row[1]
        subtype_en = row[2]
        variant_cs = row[3][0].upper() + row[3][1:].lower()
        variant_en = row[4][0].upper() + row[4][1:].lower()
        solution_methods_cs = [{"solution_name": row[5], "file_name": row[8] + ".txt"}]
        solution_methods_en = [{"solution_name": row[6], "file_name": row[8] + "_en.txt"}]
        num_of_solutions = row[7]
        svg = row[9]
        new_task = Task(type, subtype_cs, subtype_en, variant_cs, variant_en, solution_methods_cs, solution_methods_en, num_of_solutions, svg)
        for i_task in tasks.get(type, []):
            if i_task.variant_cs == new_task.variant_cs:
                merged_task = merge_tasks(i_task, new_task)
                tasks[type].remove(i_task)
                tasks[type] = tasks.get(type, []) + [merged_task]
                break
        else:
            tasks[type] = tasks.get(type, []) + [new_task]

