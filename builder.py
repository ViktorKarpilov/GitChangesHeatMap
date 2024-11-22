import subprocess
from pathlib import Path


def initiate():

    root = Path(__file__).parent
    web = root / 'web_interface'
    src = web / 'src'
    app = src / 'app.ts'
    temp = root / 'temp.js'
    html_template  = src / 'index.html'
    web_components_template = web / 'web_components_template.py'
    web_components = web / 'web_components.py'

    subprocess.run([
        'esbuild',
        app,
        '--bundle',
        '--minify=false',
        f'--outfile={temp}'
    ], shell=True, check=True)

    with open(temp, 'r') as f:
        js_code = f.read()

    with open(html_template, 'r') as f:
        html = f.read().replace('{{js_code}}', js_code)

    with open(web_components_template, 'r') as f:
        web_component_content = f.read()
        web_component_content = web_component_content.replace('#HTML_CONTENT#', html)

    with open(web_components, 'w') as f:
        f.write(web_component_content)

if __name__ == "__main__":
    initiate()