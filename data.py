import csv
import unicodedata
import re

# Create a hyperlink to another task from variant name
# @param variant - (string) name of the task
# @param tasks - (dictionary) with all tasks
# @param lang - language we want it in
def get_path_from_variant(variant, tasks, lang):
    for task_type, type_tasks in tasks.items():
        for task in type_tasks:
            if task.get_variant(lang) == variant:
                return task.get_type(lang) + "/"+ task.get_path_name(lang)

# Gather all information about each individual task
class Task():

    path_base = "src/task_data/"
    path_folder = "/task_data/"

    def __init__(self, task_type, variant_cs, variant_en, solution_methods_cs, solution_methods_en, num_of_solutions, svg, linecount):
        self.correct_data = True
        # Task task_type doesn't match the correct form
        if not re.match(r"[bkp][bkp][bkp]", task_type):
            print(f"Incorrect task_type: {task_type}. On line {linecount} in CSV file")
            self.correct_data = False
        else: self.task_type = task_type
        # Czech variant is unset
        if len(variant_cs) == 0:
            print(f"Incorrect variant_cs: {variant_cs}. On line {linecount} in CSV file")
            self.correct_data = False
        else: self.variant_cs = variant_cs
        # English variant is unset
        if len(variant_en) == 0:
            print(f"Incorrect variant_en: {variant_en}. On line {linecount} in CSV file")
            self.correct_data = False
        else: self.variant_en = variant_en
        # Czech solution method is unset
        if len(solution_methods_cs) == 0:
            print(f"Incorrect solution_method_cs: {solution_methods_cs}. On line {linecount} in CSV file")
            self.correct_data = False
        else: self.solution_methods_cs = solution_methods_cs
        # English solution method is unset
        if len(solution_methods_en) == 0:
            print(f"Incorrect solution_method_en: {solution_methods_en}. On line {linecount} in CSV file")
            self.correct_data = False
        else: self.solution_methods_en = solution_methods_en
        # Number of solution is not an integer
        if not (num_of_solutions.isdigit() or num_of_solutions == "Nekonečno"):
            print(f"Incorrect num_of_solutions: {num_of_solutions}. On line {linecount} in CSV file")
            self.correct_data = False
        else: self.num_of_solutions = num_of_solutions
        if len(svg) == 0:
            print(f"Incorrect svg: {svg}. On line {linecount} in CSV file")
            self.svg = ""
            # self.correct_data = False
        else: self.svg = svg

    def get_type(self, lang):
        if lang == "cs":
            return self.task_type
        elif lang == "en":
            # Translate czech letters to english (Přímka -> Line)
            return self.task_type.replace("p", "l").replace("k", "c").replace("b", "p")

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

        # Replace accent characters
        path = unicodedata.normalize('NFD', variant).encode('ascii', 'ignore').decode("utf-8")
        # Replace unwanted characters
        chars_to_remove = [",", ".", ";", "-", "_", "/", "\\"]
        for char in chars_to_remove:
            path = path.replace(char, "")
        # Replace spaces
        path = path.replace(" ", "-")
        path = path.lower()
        return path

    def get_full_type(self, lang):
        if lang == "cs":
            return self.task_type.replace("b", "BOD ").replace("k", "KRUŽNICE ").replace("p", "PŘÍMKA ").rstrip().replace(" ", " • ")
        elif lang =="en":
            return self.task_type.replace("b", "POINT ").replace("k", "CIRCLE ").replace("p", "LINE ").rstrip().replace(" ", " • ")

    def get_geogebra_file_path(self, file_name):
        
        ggb_file_name = file_name.replace(".txt",".ggb").replace("_en.ggb",".ggb")
        return Task.path_folder + self.task_type.upper() + "/" + ggb_file_name



    def get_construction_steps(self, file_name, tasks, lang):
        text_file_path = Task.path_base + self.task_type.upper() + "/" + file_name
        # text_file_path = "src/task_data/BPP/bpp_ruznobezky_bod_mimo_primky.txt" # Correctly formated file as a placeholder
        try:
            with open(text_file_path, mode="r", encoding="utf-8") as file_steps:
                pre_steps = file_steps.read()
                pre_steps = pre_steps.split("\n")
                steps = []
                for step in pre_steps:
                    if len(step) == 0:
                        continue

                    # Set lower indices
                    # Doesn't start with a whitespace char or asterisk, then underscore, then until whitespace or asterisk
                    # k_1 / B_a / C_123
                    indices_regex = re.compile(r" ([^\*\s]+)_([^\*\s]+) ", re.VERBOSE)
                    step = re.sub(indices_regex, r"\1<sub>\2</sub>", step)
                    # Set italic parts
                    open_tag = True
                    while "*" in step:
                        if open_tag:
                            step = step.replace("*", "<i>", 1)
                        elif not open_tag:
                            step = step.replace("*", "</i>", 1)
                        open_tag = not open_tag

                    # Set hyperlinks to other tasks
                    for hyper_variant in re.findall(r"\[(.+)\]", step):
                        hyper_path = get_path_from_variant(hyper_variant, tasks, lang)
                        step = re.sub(r"\[(.+\])", rf"<a href=../../{hyper_path} class='underline text-primary'>\1", step, 1)
                    step = step.replace("]", "</a>")

                    # Delete numbered lists
                    if step[0].isdigit():
                        # Step starts with number, take string from first space
                        step = step[step.index(" "):]

                    steps.append(step.strip())
        except:
            print(f"Missing file with steps - {self.get_variant('cs')}")
            steps = ["Chybí postup"]
        return steps

    def get_same_type_tasks(self, tasks, lang):
        same_type_tasks = tasks[self.task_type.lower()]
        result_data = []
        for task in same_type_tasks:
            if task != self:
                result_data.append(task)
        return result_data

    def get_svg(self):
        if len(self.svg) > 0:
            return self.svg
        # Set placeholder question mark
        else:
            return '<svg width=\"15\" height=\"23\" viewBox=\"0 0 15 23\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M9.24316 15.2471H5.03906C5.03906 14.3877 5.09766 13.6309 5.21484 12.9766C5.3418 12.3125 5.55664 11.7168 5.85938 11.1895C6.16211 10.6621 6.57227 10.1738 7.08984 9.72461C7.54883 9.34375 7.94434 8.97754 8.27637 8.62598C8.6084 8.27441 8.8623 7.91797 9.03809 7.55664C9.21387 7.19531 9.30176 6.80957 9.30176 6.39941C9.30176 5.8916 9.22852 5.47656 9.08203 5.1543C8.94531 4.83203 8.73535 4.59277 8.45215 4.43652C8.17871 4.27051 7.83203 4.1875 7.41211 4.1875C7.07031 4.1875 6.74805 4.27051 6.44531 4.43652C6.15234 4.60254 5.91309 4.86133 5.72754 5.21289C5.54199 5.55469 5.43945 6.00879 5.41992 6.5752H0.454102C0.483398 5.12012 0.805664 3.93848 1.4209 3.03027C2.0459 2.1123 2.87598 1.44336 3.91113 1.02344C4.95605 0.59375 6.12305 0.378906 7.41211 0.378906C8.83789 0.378906 10.0635 0.598633 11.0889 1.03809C12.1143 1.47754 12.9004 2.13184 13.4473 3.00098C13.9941 3.86035 14.2676 4.91992 14.2676 6.17969C14.2676 7.01953 14.1064 7.75195 13.7842 8.37695C13.4717 8.99219 13.0469 9.56836 12.5098 10.1055C11.9824 10.6328 11.3916 11.1992 10.7373 11.8047C10.1709 12.3027 9.78516 12.8105 9.58008 13.3281C9.375 13.8359 9.2627 14.4756 9.24316 15.2471ZM4.43848 19.7002C4.43848 18.9971 4.69238 18.4111 5.2002 17.9424C5.70801 17.4639 6.36719 17.2246 7.17773 17.2246C7.98828 17.2246 8.64746 17.4639 9.15527 17.9424C9.66309 18.4111 9.91699 18.9971 9.91699 19.7002C9.91699 20.4033 9.66309 20.9941 9.15527 21.4727C8.64746 21.9414 7.98828 22.1758 7.17773 22.1758C6.36719 22.1758 5.70801 21.9414 5.2002 21.4727C4.69238 20.9941 4.43848 20.4033 4.43848 19.7002Z\" fill=\"black\"/></svg>'

# Merge multiple solution methods into one task
def merge_tasks(task1, task2):
    task1.solution_methods_cs.extend(task2.solution_methods_cs)
    task1.solution_methods_en.extend(task2.solution_methods_en)
    return task1



# Opening tasks_data.csv file with task data - from the excel sheets

tasks = {}
with open("src/tasks_data.csv", mode="r", encoding="utf-8") as data_file:
    csv_reader = csv.reader(data_file, delimiter=";")

    header = csv_reader.next() # first row = header
    csv_reader.next()          # second row = notes


    linecount = 3      # starting row number (counting from 1)
    for row in csv_reader:
        
        task_type = "".join(sorted(row[0].lower())) # Sort letters alphabetically to unify it

        variant_cs = row[1].capitalize() # Capital first letter
        if len(row[2]) != 0:
            variant_en = row[2].title() # Capital first letter of each word (as in titles in English)
        else: 
            variant_en = "English Title Missing - " + variant_cs

        solution_methods_cs = [{"solution_name": row[3], "file_name": row[6] + ".txt"}] # List in case there are more methods
        if row[4] == "": 
            row[4] = "English method missing"
        solution_methods_en = [{"solution_name": row[4], "file_name": row[6] + "_en.txt"}] # List in case there are more methods
        num_of_solutions = row[5]

        svg = row[10]
        new_task = Task(task_type, variant_cs, variant_en, solution_methods_cs, solution_methods_en, num_of_solutions, svg, linecount)

        if new_task.correct_data: # if every piece of data is correct
            merging = False
            for i_task in tasks.get(task_type, []):
                # If task with same name already exists, merge them (different solution method)
                if i_task.variant_cs == new_task.variant_cs:
                    merged_task = merge_tasks(i_task, new_task)
                    tasks[task_type].remove(i_task)
                    tasks[task_type] = tasks.get(task_type, []) + [merged_task]
                    merging = True

            # Execute if loop didn't encounter merging
            if not merging:
                tasks[task_type] = tasks.get(task_type, []) + [new_task]
        
        linecount += 1

