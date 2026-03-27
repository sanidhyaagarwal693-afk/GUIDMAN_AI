import json


class GuideEngine:

    def __init__(self):

        self.guides = {
            "github repo": "guides/github_repo.json",
            "create repo": "guides/github_repo.json",
            "github": "guides/github_repo.json",

            "chrome devtools": "guides/chrome_devtools.json",
            "open devtools": "guides/chrome_devtools.json",

            "vscode extension": "guides/vscode_extension.json",
            "install extension": "guides/vscode_extension.json"
        }

    def find(self, text):

        text = text.lower()

        for key in self.guides:

            if key in text:
                return self.guides[key]

        return None

    def load(self, path):

        with open(path) as f:
            return json.load(f)