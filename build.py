from jinja2 import Environment, FileSystemLoader
import shutil


def makeEnv():
    file_loader = FileSystemLoader('src/templates')
    env = Environment(loader=file_loader)
    return env

def render_categories(save_path):
    env = makeEnv()
    categories_template = env.get_template("cs/categories.jinja2")

    output = categories_template.render()
    with open(save_path, mode="w", encoding="utf-8") as file_output:
        file_output.write(output)


render_categories("dist/index.html")

shutil.rmtree("dist/js")
shutil.copytree("src/js", "dist/js")

shutil.rmtree("dist/assets")
shutil.copytree("src/assets", "dist/assets")
