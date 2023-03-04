# pdoc3
# https://pdoc3.github.io/pdoc/

find make helpers.py -name "*.py" -exec pdoc --force "{}" -o docs/makers/ \;
./makedoc.py > docs/recipes.md

