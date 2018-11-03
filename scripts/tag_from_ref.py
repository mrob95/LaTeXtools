import re

def get_tag(ref):
    query = re.compile(r'@.*{(.*),')
    tag = re.search(query, ref)
    if tag:
        return tag.group(1)
    else:
        return "No tag found"
