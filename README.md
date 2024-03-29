# Apollonius

Web vysvětlující všechny případy apolloniových úloh.

# Build

You might have to manually create some folders along the way (or chage the code to do it automatically).

First, run the Python build script to build the website:

```
python3 build.py
```

You might have to reinstall some dependencies, follow the instructions (errors) in terminal.

Next, build the Tailwind CSS with:

```
npx tailwindcss -i src/scss/input.scss -o dist/css/output.css --watch
```

`--watch` rebuilds the css as you change it during development.

# Deployment

After building the website, copy the `dist` folder to server (remove the `-n` flag):

```
rsync -anv --progress ./dist/ adam@ctb6.metactrl.com:/var/www/apollonea.com
```
