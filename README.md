# Apollonius

Web vysvětlující všechny případy apolloniových úloh.

# Build

DISCLAIMER: You might have to manually create some folders along the way (or chage the code to do it automatically).

First, run the Python build script to build the website:

```
python3 build.py
```

You might have to reinstall some dependencies, follow the instructions (errors) in terminal.

Next, build the Tailwind CSS with:

```
npx tailwindcss -i src/scss/input.scss -o dist/css/output.css --watch
```

# Deployment

Copy the `dist` folder to server:

```
scp -r ./dist adam@178.18.251.189:/var/www/apollonea.com/www
```
