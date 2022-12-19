from jinja2 import Environment, FileSystemLoader
import shutil
from data import tasks
import os
import glob
import json

def makeEnv():
    file_loader = FileSystemLoader('src/templates')
    env = Environment(loader=file_loader)
    return env

def render_categories():
    env = makeEnv()
    categories_template = env.get_template("categories.jinja2")

    languages = {}

    translation_paths = glob.glob("src/translations/categories*.json")

    for translation_path in translation_paths:
        filename = os.path.basename(translation_path)
        lang_code = filename.split(".")[0].split("_")[1]

        with open(f"src/translations/{filename}", mode="r", encoding="utf-8") as translation_file:
            languages[lang_code] = json.load(translation_file)

    output_cs = categories_template.render(**languages["cs"])
    with open("dist/cs/index.html", mode="w", encoding="utf-8") as file_output:
        file_output.write(output_cs)
    output_en = categories_template.render(**languages["en"])
    with open("dist/en/index.html", mode="w", encoding="utf-8") as file_output:
        file_output.write(output_en)

def render_subcategories():
    env = makeEnv()
    # czech template
    subcategories_template_cs = env.get_template("subcategories.jinja2")

    for type, type_tasks in tasks.items():
        output_cs = subcategories_template_cs.render(type_tasks=type_tasks)
        if not os.path.exists(f"dist/cs/{type}"):
            os.makedirs(f"dist/cs/{type}")
        with open(f"dist/cs/{type}/index.html", mode="w", encoding="utf-8") as file_output:
            file_output.write(output_cs)

def render_tasks():
    env = makeEnv()
    tasks_template_cs = env.get_template("task.jinja2")

    for type, type_tasks in tasks.items():
        for task in type_tasks:
            with open("src/bbp_rovnobezky_bod_na_primce.txt", mode="r", encoding="utf-8") as file_steps:
                pre_steps = file_steps.read()
                pre_steps = pre_steps.split("\n")
                steps = []
                for step in pre_steps:
                    if len(step) == 0:
                        continue
                    steps.append(step[step.index(".")+1:].strip())

            output_cs = tasks_template_cs.render(task=task, steps=steps)
            if not os.path.exists(f"dist/cs/{type}/{task.get_path_name_cs()}"):
                os.makedirs(f"dist/cs/{type}/{task.get_path_name_cs()}")
            with open(f"dist/cs/{type}/{task.get_path_name_cs()}/index.html", mode="w", encoding="utf-8") as file_output:
                file_output.write(output_cs)


render_categories()
render_subcategories()
render_tasks()

shutil.rmtree("dist/js")
shutil.copytree("src/js", "dist/js")

shutil.rmtree("dist/assets")
shutil.copytree("src/assets", "dist/assets")
