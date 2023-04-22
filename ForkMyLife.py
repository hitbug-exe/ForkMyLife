import os
from git.repo.base import Repo
import markdown
from giturlparse import parse
import pynliner
import tempfile
from pathlib import Path
import json
import subprocess
import argparse


def DirectoryName (url):
  p = parse(url)
  return p.repo

def AuthorName (url):
  p = parse(url)
  return p.owner

def DirectoryHTTPS(url):
  p = parse(url)
  return p.url2https

def CreateDirectory(dname):
  parent_dir = "repos/"
  path = os.path.join(parent_dir, dname)
  rpath = os.path.join("resources/", dname)
  os.mkdir (path)
  os.mkdir (rpath)
  return 0

def CloneRepo(url):
  https = DirectoryHTTPS(url)
  dname = DirectoryName(url)
  CreateDirectory(dname)
  dir = "repos/" + dname
  Repo.clone_from(https, dir)
  return 0


def MDtoHTML(url, title, author):
    dname = DirectoryName(url)
    CloneRepo(url)
    path = "repos/" + dname + "/README.md"
    with open(path, 'r') as f:
        text = f.read()
        text = text + "\n [Access the full source code here]" + "(" + DirectoryHTTPS(url) + ")"
        html = markdown.markdown(text)

    with open("resources/styles.css", 'r') as f:
        css = f.read()

    # Add header and body tags to HTML string
    header = f"<header style='background-color:#1f1f1f; color:#f0f0f0; padding:10px 20px; display:flex; justify-content:space-between; align-items:center; margin-bottom:30px'><h1>{title}</h1><p>Author: {author}</p></header>"
    body = f"<body style='background-color:#0d0d0d;color:rgb(248, 248, 248);'>{html}</body>"
    html = f"<html>{header}{body}</html>"

    p = pynliner.Pynliner()
    inHTML = p.from_string(html).with_cssString(css).run()

    return inHTML

def deploy_to_vercel(html_content: str, project_name: str, vercel_token: str):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set the project directory
        project_dir = Path(temp_dir) / project_name
        os.makedirs(project_dir)

        # Write the HTML content to the index.html file
        with open(project_dir / "index.html", "w") as f:
            f.write(html_content)

        # Write the vercel.json configuration file
        vercel_config = {
            "name": project_name,
            "version": 2,
            "builds": [{"src": "index.html", "use": "@vercel/static"}],
        }

        with open(project_dir / "vercel.json", "w") as f:
            json.dump(vercel_config, f)

        # Deploy to Vercel using the CLI
        cmd = ["vercel", "--token", vercel_token, "-y", "--prod"]

        result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True)

        if result.returncode == 0:
            print("Deployment successful!")
            print(f"Deployment URL: {result.stdout.strip()}")
        else:
            print("Deployment failed:")
            print(result.stderr)

def main():
    parser = argparse.ArgumentParser(description='ForkMyLife. Your Github README.md on steroids.')
    parser.add_argument('url', type=str, help='the URL of the public git repository')
    parser.add_argument('vercel_token', type=str, help='the Vercel API token')
    args = parser.parse_args()

    url = args.url
    vercel_token = args.vercel_token

    html = MDtoHTML(url, DirectoryName(url), AuthorName(url))
    deploy_to_vercel(html, DirectoryName(url), vercel_token)

if __name__ == '__main__':
    main()

  