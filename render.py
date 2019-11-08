import json
from staticjinja import Site

if __name__ == "__main__":
    with open('data.json', 'r') as file:
        context = {
            'news' : json.loads(file.read()),
        }
    site = Site.make_site(env_globals=context)

    site.render(use_reloader = True)