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

def get_translation(sections, lang):
    language = {}
    for section in sections:
        translation_path = glob.glob(f"src/translations/{section}_{lang}.json")[0]
        with open(translation_path, mode="r", encoding="utf-8") as file:
            language.update(json.load(file))
    return language

def render_categories():
    env = makeEnv()
    categories_template = env.get_template("categories.jinja2")

    langs = {"cs": "dist/cs", "en":"dist/en"}

    for lang, lang_path in langs.items():
        translation = get_translation(["main", "categories"], lang)
        translation.update(langs)
        output = categories_template.render(**translation)
        with open(f"{lang_path}/index.html", mode="w", encoding="utf-8") as file_output:
            file_output.write(output)

def render_subcategories():
    env = makeEnv()
    subcategories_template = env.get_template("subcategories.jinja2")

    langs = {"cs": "dist/cs", "en":"dist/en"}

    for lang, lang_path in langs.items():
        translation = get_translation(["main"], lang)
        translation.update(langs)
        for type, type_tasks in tasks.items():
            output = subcategories_template.render(type_tasks=type_tasks, **translation)
            if not os.path.exists(f"{lang_path}/{type_tasks[0].get_type(lang)}"):
                os.makedirs(f"{lang_path}/{type_tasks[0].get_type(lang)}")
            with open(f"{lang_path}/{type_tasks[0].get_type(lang)}/index.html", mode="w", encoding="utf-8") as file_output:
                file_output.write(output)

def render_tasks():
    env = makeEnv()
    tasks_template = env.get_template("task.jinja2")

    langs = {"cs": "dist/cs", "en":"dist/en"}

    for lang, lang_path in langs.items():
        translation = get_translation(["main", "task"], lang)
        translation.update(langs)

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

                output = tasks_template.render(type_tasks=type_tasks, task=task, steps=steps, **translation)
                if not os.path.exists(f"{lang_path}/{task.get_type(lang)}/{task.get_path_name(lang)}"):
                    os.makedirs(f"{lang_path}/{task.get_type(lang)}/{task.get_path_name(lang)}")
                with open(f"{lang_path}/{task.get_type(lang)}/{task.get_path_name(lang)}/index.html", mode="w", encoding="utf-8") as file_output:
                    file_output.write(output)


render_categories()
render_subcategories()
render_tasks()

shutil.rmtree("dist/js")
shutil.copytree("src/js", "dist/js")

shutil.rmtree("dist/assets")
shutil.copytree("src/assets", "dist/assets")
