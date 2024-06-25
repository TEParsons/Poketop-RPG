import re
from mkdocs.structure import pages, files
from mkdocs import config
from functools import partial


site_url = "/"
source_dir = "/"


def substitute_root_link(to_root: str, match: re.Match) -> str:
    """
    Make a root link (beginning with a slash) relative to the *site* root rather than the **server* root.

    Parameters
    ----------
    match : re.Match
        Regex match for the link
    """
    # get all groups
    label, link = match.groups()
    # remove start if link includes root folder
    for pre in ("source/", ):
        if link.startswith(pre):
            link = link[len(pre):]
    # construct full link
    full_link = f"[{label}]({to_root}/{link})"

    return full_link


def on_page_markdown(markdown: str, page: pages.Page, config: config.Config, files: files.File) -> str:
    """
    Make links beginning with a slash relative to the *site* root rather than the *server* root.

    Parameters
    ----------
    markdown : str
        Markdown text
    page : pages.Page
        MkDocs page object
    config : config.Config
        MkDocs configutation object
    files : files.File
        MkDocs file object

    Returns
    -------
    str
        Parsed markdown text
    """
    # construct relative path to root
    num_back = page.file.src_uri.count("/")
    if page.file.name != "index":
        num_back += 1
    to_root = "/".join([".."] * num_back)
    # pre-populate substitution function with relative root string
    repl = partial(substitute_root_link, to_root)
    # regex to find root links
    re_link = r"\[([^\]]*)\]\(\/([^\)]*)\)"
    # do substitution
    return re.sub(
        pattern=re_link,
        string=markdown, 
        repl=repl
    )