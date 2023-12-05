import re 
import os 
import csv 
from tqdm import tqdm 
import functools 


DIR_ROOT= os.path.dirname(os.path.abspath(__file__))
COLLECTION_CSV = os.path.join(DIR_ROOT, 'awesome-list.csv')
MD_FILE= os.path.join(DIR_ROOT, 'README.md')

HEAD = f"""# Awesome-Instruction-Prompted-Vision
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

A curated list of instruction-prompted visual translation papers and resources, inspired by [awesome-image-inpainting](https://github.com/zengyh1900/Awesome-Image-Inpainting).

![](https://s2.loli.net/2023/12/05/HTrWELGOtlPwQCg.png)

<table>
  <tr>
    <td>
      <img src="assets/origin.gif" width="100%" />
      <br>
      <p>Original NeRF</p>
    </td>
    <td>
      <img src="assets/desert.gif" width="100%" />
      <br>
      <p>"Make it look like the Namibian desert"</p>
    </td>
    <td>
      <img src="assets/sunset.gif" width="100%" />
      <br>
      <p>"Make it sunset"</p>
    </td>
  </tr>
</table>


This `README.md` is automatically generated from [`awesome-list.csv`](awesome-list.csv). 

We provide [scripts](generate.py) to automatically generate `README.md` from CSV file or vice versa. 

Welcome to pull request to update or correct this collection.
"""


def csv_to_readme():
    # save all data to csv file 
    csvfile = open(COLLECTION_CSV)
    csv_reader = csv.reader(csvfile, delimiter=',')
    
    papers = {}
    # parse data from csv file 
    for idx, row in enumerate(csv_reader):
        if idx == 0:
            continue 
        year, conf, type, title, url, code, project, _ = row 
        p = dict(title=title, url=url, conf=conf, year=year, project=project, code=code, type=type)
        if str(type) not in papers: 
            papers[str(type)] = [p]
        else:
            papers[str(type)].append(p)
    
    for k, v in papers.items(): 
        papers[k].sort(key=lambda x: (x['year'], x['conf'], x['type']), reverse=True)
    
    message = {}
    # generate msg from parsed dict data
    modal = ['Image', '3D', 'Video', 'Multiple']
    for k,v in papers.items():
        msg = f"## {k}\n"
        for p in v: 
            msg += f"- **{p['conf']}** ({p['year']}) [{p['title']}]({p['url']})."
            if p['code']:
                git_user = p['code'].split('/')[-2]
                git_repo = p['code'].split('/')[-1]
                msg += f" [![Star](https://img.shields.io/github/stars/{git_user}/{git_repo}.svg?style=social&label=Star)]({p['code']})"
            if p['project']:
                msg += f" [![Website](https://img.shields.io/badge/Website-100)]({p['project']}) "
            msg += "\n"
        message[k] = msg 
    
    # write to readme 
    readme_content = HEAD
    for y in modal: 
        readme_content += message[y]
    with open(MD_FILE, 'w') as f:
        f.write(readme_content)


if __name__ == '__main__':
    csv_to_readme()