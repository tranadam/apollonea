from jinja2 import Environment, FileSystemLoader
import shutil
from data import tasks
import os
import glob
import json


# Create enviroment for Jinja template rendering
def makeEnv():
    file_loader = FileSystemLoader('src/templates')
    env = Environment(loader=file_loader)
    return env

# Retrieve texts for a page in given language
# @param pages - (array) names of pages
# @param lang - (string) chosen language (cs/en)
def get_translation(pages, lang):
    language = {}
    for section in pages:
        translation_path = glob.glob(f"src/translations/{section}_{lang}.json")[0]
        with open(translation_path, mode="r", encoding="utf-8") as file:
            language.update(json.load(file))
    return language

# Generate redirect page
def render_redirect():
    env = makeEnv()
    redirect_template = env.get_template("redirect.jinja2")
    translation = get_translation(["main"], "en")
    output = redirect_template.render(**translation)
    with open("dist/index.html", mode="w", encoding="utf-8") as file_output:
        file_output.write(output)

# Generate HTML files for Categories/Landing page in all languages
def render_categories():
    env = makeEnv()
    categories_template = env.get_template("categories.jinja2")

    langs = {"cs": "dist/cs", "en":"dist/en"}

    for lang, lang_path in langs.items():
        if not os.path.exists(lang_path):
            os.makedirs(lang_path)
        translation = get_translation(["main", "categories"], lang)
        translation.update(langs)
        output = categories_template.render(**translation)
        with open(f"{lang_path}/index.html", mode="w", encoding="utf-8") as file_output:
            file_output.write(output)

# Generate HTML files for all subcategories in all languages
def render_subcategories():
    env = makeEnv()
    subcategories_template = env.get_template("subcategories.jinja2")

    langs = {"cs": "dist/cs", "en":"dist/en"}

    for lang, lang_path in langs.items():
        translation = get_translation(["main","subcategories"], lang)
        translation.update(langs)

        for type, type_tasks in tasks.items():
            output = subcategories_template.render(type_tasks=type_tasks, **translation)
            if not os.path.exists(f"{lang_path}/{type_tasks[0].get_type(lang)}"):
                os.makedirs(f"{lang_path}/{type_tasks[0].get_type(lang)}")
            with open(f"{lang_path}/{type_tasks[0].get_type(lang)}/index.html", mode="w", encoding="utf-8") as file_output:
                file_output.write(output)

# Render HTML files for each individual task in all languages
def render_tasks():
    env = makeEnv()
    tasks_template = env.get_template("task.jinja2")

    langs = {"cs": "dist/cs", "en":"dist/en"}

    for lang, lang_path in langs.items():
        translation = get_translation(["main", "task"], lang)
        translation.update(langs)

        for type, type_tasks in tasks.items():
            for task in type_tasks:
                output = tasks_template.render(tasks=tasks, task=task, **translation)
                if not os.path.exists(f"{lang_path}/{task.get_type(lang)}/{task.get_path_name(lang)}"):
                    os.makedirs(f"{lang_path}/{task.get_type(lang)}/{task.get_path_name(lang)}")
                with open(f"{lang_path}/{task.get_type(lang)}/{task.get_path_name(lang)}/index.html", mode="w", encoding="utf-8") as file_output:
                    file_output.write(output)

render_redirect()
render_categories()
render_subcategories()
render_tasks()

shutil.rmtree("dist/assets")
shutil.copytree("src/assets", "dist/assets")

shutil.rmtree("dist/task_data")
shutil.copytree("src/task_data", "dist/task_data")
