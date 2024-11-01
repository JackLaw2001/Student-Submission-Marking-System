import os
from glob import glob 
import pandas as pd
from bs4 import BeautifulSoup
from utils import *
from args import *
import markdown

def marking(dirns):
    """
    Grades student submissions in specified directories.

    Parameters:
        dirns (list): A list of directory paths containing student submissions.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: A DataFrame with assessment information for each student.
            - str: A concatenated string of markdown content for all students.
    """
    promptGitM = read_text_file(os.path.join(prompts_dir, 'GitM.txt'))
    promptCODE = read_text_file(os.path.join(prompts_dir, 'CODE.txt'))
    promptREPORT = read_text_file(os.path.join(prompts_dir, 'REPORT.txt'))
    promptPANDA = read_text_file(os.path.join(prompts_dir, 'PANDA.txt'))
    GitMMarker = GPTMarker(promptGitM, [1,1,1,1])
    CODEMarker = GPTMarker(promptCODE, [1,1])
    REPORTMarker = GPTMarker(promptREPORT, [1,1,2])
    PANDAMarker = GPTMarker(promptPANDA, [3,1])
    
    assinfos = []
    markdowns = []
    for dirn in dirns:

        ### Step 1: Extract all neccessary information from the folder

        print('Processing Folder: {}'.format(dirn))

        # Extract files if neccessary
        if count_files_in_directory(dirn) < 5:
            all_fns = glob(os.path.join(dirn, '*'))
            non_txt_fns = [f for f in all_fns if not f.endswith('.txt')]
            extract_file(non_txt_fns[0])

        marking = {}
        studinfo = parse_student_info(find_files_with_suffix('StudInfo.txt', dirn)[0])
        print('Student Name: {} ({})'.format(studinfo['Name'], studinfo['ID']))

        # The following are handling markdown files
        mdfiles = find_files_with_suffix('.md', dirn)
        mdfilesplit = [os.path.split(x)[1] for x in mdfiles]

        if 'LICENSE.md' in mdfilesplit:
            LICENSEmd = read_text_file(find_files_with_suffix('LICENSE.md', dirn)[0])
        else:
            LICENSEmd = -1
            print('LICENSE.md Not Found')

        if 'README.md' in mdfilesplit:
            READMEmd = read_text_file(find_files_with_suffix('README.md', dirn)[0])
        else:
            READMEmd = -1
            print('README.md Not Found')  

        mdfilesplit = [x for x in mdfilesplit if (x != 'LICENSE.md') and (x != 'README.md') and (x != 'CODE_OF_CONDUCT.md')]

        if len(mdfilesplit) == 1:
            REPORTmd = read_text_file(find_files_with_suffix(mdfilesplit[0], dirn)[0])
            html = markdown.markdown(REPORTmd)
            soup = BeautifulSoup(html, 'html.parser')
            plain_text = soup.get_text()
            REPORTCount = len(plain_text.split())
        elif len(mdfilesplit) == 0:
            REPORTmd = -1
        else:
            REPORTind = [x for x in mdfilesplit if 'report' in x.lower()]
            if len(REPORTind) == 0:
                REPORTmd = -2
            else:
                REPORTmd = read_text_file(find_files_with_suffix(REPORTind[0], dirn)[0])
                html = markdown.markdown(REPORTmd)
                soup = BeautifulSoup(html, 'html.parser')
                plain_text = soup.get_text()
                REPORTCount = len(plain_text.split())
        InDoc = 1 if len(find_files_with_suffix('doc/*.md', dirn)) != 0 else 0

        # Check requirements.txt
        reqfs = find_files_with_suffix('requirements.txt', dirn)
        REQ = 0
        REQS = -1
        if len(reqfs) != 0:
            REQS = read_text_file(reqfs[0])
            for reqf in reqfs:
                if 'panda3d' in read_text_file(reqf):
                    REQ = 1
                    REQS = read_text_file(reqf)
                    break

        # Git Commit Messages
        gitm = glob(os.path.join(dirn,'**','.git','logs','HEAD'))
        if len(gitm) == 0:
            GitM = -1
        else:
            GitM = extract_commit_info(gitm[0])
            GitM = '\n'.join(GitM)

        # Code
        pypath = find_files_with_suffix('walking_panda.py', dirn)[0]
        CODE = ' '.join(['\n# Path:' + path + '\n' + read_text_file(path) for path in find_files_with_suffix('.py', dirn) if 'venv' not in path])
        ARGUCount = CODE.count('parser.add_argument')

        # Directory Structure
        dirstru = get_directory_structure(dirn)
        VENV = -1 if len(find_files_with_suffix('venv/*', dirn)) > 0 else 0

        assinfo = {'Name':studinfo['Name'],\
                  'ID':studinfo['ID'],\
                  'Email':studinfo['Email'],\
                  'Tutor':studinfo['Tutor'],\
                   'PythonPath':pypath,\
                   'LICENSE':LICENSEmd,\
                  'README':READMEmd,\
                  'REPORT':REPORTmd,\
                   'REPORTWORDCount':REPORTCount,\
                  'REQUIREMENTS':REQS,\
                  'InREQ':REQ,\
                   'InDoc':InDoc,\
                  'GitM':GitM,\
                   'CODE':CODE,\
                   'ARGUCount':ARGUCount,\
                  'VENV':VENV,\
                  'DSD':dirstru}

        ### Step 2: Marking

        # ChatGPT markers
        GitMmark = GitMMarker(assinfo) if GitM != -1 else [0,0,0,0]
        CODEmark = CODEMarker(assinfo) if (READMEmd != -1) and (CODE != -1) else [0,0]
        REPORTmark = REPORTMarker(assinfo) if (REPORTmd != -1) else [0,0,0]
        PANDAmark = PANDAMarker(assinfo) if (CODE != -1) else [0,0]

        marking['1.1 completed "Running Some Code" section i.e hello_world.py'] = 1
        marking['1.2 completed "Add README.md and LICENSE.md" section'] = 1 if (READMEmd != -1) and (LICENSEmd != -1) else 0
        marking['1.3 completed "Adding a Dependency" section i.e. added panda3D to requirements.txt'] = 1 if REQ == 1 else 0
        marking['1.4 [C]completed 3 panda related sections i.e. visual/window, scenery and panda (3 marks)'] = PANDAmark[0]
        marking['1.5 [C]Git: At least 4 commits i.e. hello_world, README/LICENCE, add some scenery, add a panda'] = GitMmark[0]
        marking['1.6 [C]Provided meaningful commit messages (about part 1 only)'] = GitMmark[1]

        marking['2.1 Report as a markdown file, found in doc directory'] = InDoc
        marking['2.2 [C]Good use of markdown e.g. headings'] = int(REPORTmark[0]) if (REPORTmd != -1) else 0
        marking['2.3 [C]Describe whether you have used any of the tools or equivalent tools in the past'] = REPORTmark[1]
        marking['2.4 [C]Describe how you think the tools new to you will change your development practice'] = REPORTmark[2]
        marking['2.5 Report should be between 300-500 words (+10% allowed)'] = 1 if REPORTCount > 250 else 0
        marking['2.6 [C]Git: committed and provided meaningful commit messages (about part 2 only)'] = GitMmark[2]

        marking['3.1 [C]Updated README.md'] = CODEmark[0]
        marking['3.2 [C]Included comments in code (e.g. referenced external code)'] = CODEmark[1]
        if ARGUCount > 4:
            marking['3.3 a) Argument Implementation (2 marks, 0.5 per option)'] = 2
        elif ARGUCount < 0:
            marking['3.3 a) Argument Implementation (2 marks, 0.5 per option)'] = 0
        else:
            marking['3.3 a) Argument Implementation (2 marks, 0.5 per option)'] = ARGUCount / 2
        marking['3.4 [C]A Multi-Media experience (1 mark)'] = PANDAmark[1]
        marking['3.5 [C]Git: committed and provided meaningful commit messages (about part 3 only)'] = GitMmark[3]

        marking['4 DO NOT SUBMIT INCORRECT FILES (e.g. venv)'] = VENV

        ### Step 3: Generate reports and update

        mkr = generate_markdown_report_string(marking, full_marking, studinfo, assinfo, dirn)
        mkds = '{}  \n## LICENSE.md  \n{}\n## README.md  \n{}\n## REPORT.md  \n{}\n## Git Message  \n{}\n## requirements.txt  \n{}\n## CODE  \n```python{}```'.format(mkr, LICENSEmd, READMEmd, REPORTmd, GitM, REQS, CODE)
        save_txt_file(mkds, os.path.join(markdown_dir, '{}.md'.format(studinfo['ID'])))

        assinfo.update(marking)
        assinfos.append(assinfo)
        markdowns.append(mkds)
    
    asstable = pd.DataFrame(assinfos)
    markdownsall = '  \n'.join(markdowns)
    
    return asstable, markdownsall

if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()
    check(args)
    
    root_dir = args.root_dir
    markdown_dir = args.markdown_dir
    prompts_dir = args.prompts_dir
    output_dir = args.output_dir
    openai.api_key = args.apikey if args.apikey != None else read_text_file(os.path.join(prompts_dir, 'APIkey.txt'))
    
    dirns = sorted(glob(os.path.join(root_dir, '*')))[:2]
    asstable, markdownsall = marking(dirns)
    asstable.to_csv(os.path.join(output_dir, 'marks.csv'))
    save_txt_file(markdownsall, os.path.join(output_dir, 'all.md'))
