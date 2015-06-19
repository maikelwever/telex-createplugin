#!/usr/bin/env python3

import os
import sys


README_BOILERPLATE = """# {prefixed_name}

{description}

### Usage:
To do stuff:

    !do stuff"""

PLUGINFILE_BOILERPLATE = """[Core]
Name = {capitalized_name}
Module = {name}

[Documentation]
Author = {full_name}
Version = 1.0
Website = https://github.com/{github_username}/{prefixed_name}
Description = {description}"""

PYFILE_BOILERPLATE = """from telex import plugin
# from telex.DatabaseMixin import DatabaseMixin, DbType

import tgl


class {capitalized_name}Plugin(plugin.TelexPlugin):
    \"\"\"
    {description}
    \"\"\"

    patterns = {{
        "^{{prefix}}do (.+)$": "do_stuff",
    }}

    usage = [
        "{{prefix}}do (stuff): does stuff",
    ]

    \"\"\"
    schema = {{
        'msg_id': DbType.Integer,
        'timestamp': DbType.DateTime,
        'uid': DbType.Integer,
        'chat_id': DbType.Integer,
        'username': DbType.String,
        'name': DbType.String,
        'message': DbType.String,
    }}
    primary_key = 'msg_id'
    \"\"\"

    def do_stuff(self, msg, matches):
        peer = self.bot.get_peer_to_send(msg)
        peer.send_msg("Stuff is done", reply=msg.id, preview=False)"""

REPO_JSON_BOILERPLATE = """{{
    "name": "{capitalized_name}",
    "description": "{description}",
    "version": "1.0",
    "default_enable": ["{capitalized_name}"],
    "homepage": "https://github.com/{github_username}/{prefixed_name}",
    "repo": "https://github.com/{github_username}/{prefixed_name}.git",
    "branch": "master"
}}"""

GITIGNORE_BOILERPLATE = """.venv
__pycache__
*.pyc
*.swp
*.suo
"""


def main():
    if not len(sys.argv) > 1:
        print("Please give me a name to work with (make it pythonic plz).")
        sys.exit(1)

    name = sys.argv[1]
    prefixed_name = "telex-" + name.replace('_', '-')
    print("Creating new plugin '{0}' in ./telex-{0}.".format(name))

    capitalized_name = input("Please enter the capitalized name of your plugin (eg: Network or PictureSnarfer) > ")
    description = input("Please enter a description for your plugin > ")
    full_name = input("Please enter your full name > ")
    github_username = input("Please enter your github username > ")

    data_dict = {
        'name': name,
        'prefixed_name': prefixed_name,
        'capitalized_name': capitalized_name,
        'description': description,
        'full_name': full_name,
        'github_username': github_username,
    }

    print("Writing files now...")
    os.mkdir(prefixed_name)
    repo_dir = os.path.join(prefixed_name, "repository")
    os.mkdir(repo_dir)

    with open(os.path.join(prefixed_name, "readme.md"), "w+") as f:
        f.write(README_BOILERPLATE.format(**data_dict))

    with open(os.path.join(prefixed_name, "{0}.plugin".format(name)), "w+") as f:
        f.write(PLUGINFILE_BOILERPLATE.format(**data_dict))

    with open(os.path.join(prefixed_name, "{0}.py".format(name)), "w+") as f:
        f.write(PYFILE_BOILERPLATE.format(**data_dict))

    with open(os.path.join(prefixed_name, ".gitignore".format(name)), "w+") as f:
        f.write(GITIGNORE_BOILERPLATE.format(**data_dict))

    with open(os.path.join(repo_dir, "repo.json".format(name)), "w+") as f:
        f.write(REPO_JSON_BOILERPLATE.format(**data_dict))

    os.system('touch {0}'.format(os.path.join(repo_dir, "requirements.txt")))
    os.system('touch {0}'.format(os.path.join(prefixed_name, "__init__.py")))
    os.system('git init {0}'.format(prefixed_name))
    os.system('git --git-dir={0} --work-tree={1} remote add origin git@github.com:{2}/{3}'.format(
        os.path.join(prefixed_name, ".git"), prefixed_name, github_username, prefixed_name
    ))

    print("All well and done.")


if __name__ == "__main__":
    main()
