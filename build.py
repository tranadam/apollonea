from jinja2 import Environment, FileSystemLoader
import shutil
from data import tasks
import os

def makeEnv():
    file_loader = FileSystemLoader('src/templates')
    env = Environment(loader=file_loader)
    return env

def render_categories():
    env = makeEnv()
    # czech template
    categories_template_cs = env.get_template("cs/categories.jinja2")
    # english template

    # output czech template
    output_cs = categories_template_cs.render()
    with open("dist/cs/index.html", mode="w", encoding="utf-8") as file_output:
        file_output.write(output_cs)
    #output english template

def render_subcategories():
    env = makeEnv()
    # czech template
    subcategories_template_cs = env.get_template("cs/subcategories.jinja2")

    for type, type_tasks in tasks.items():
        output_cs = subcategories_template_cs.render(type_tasks=type_tasks)
        if not os.path.exists(f"dist/cs/{type}"):
            os.makedirs(f"dist/cs/{type}")
        with open(f"dist/cs/{type}/index.html", mode="w", encoding="utf-8") as file_output:
            file_output.write(output_cs)




render_categories()
render_subcategories()

shutil.rmtree("dist/js")
shutil.copytree("src/js", "dist/js")

shutil.rmtree("dist/assets")
shutil.copytree("src/assets", "dist/assets")
