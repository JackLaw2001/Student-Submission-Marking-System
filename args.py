import argparse
import os
import sys

full_marking = {'1.1 completed "Running Some Code" section i.e hello_world.py':1,\
'1.2 completed "Add README.md and LICENSE.md" section':1,\
'1.3 completed "Adding a Dependency" section i.e. added panda3D to requirements.txt':1,\
'1.4 [C]completed 3 panda related sections i.e. visual/window, scenery and panda (3 marks)':3,\
'1.5 [C]Git: At least 4 commits i.e. hello_world, README/LICENCE, add some scenery, add a panda':1,\
'1.6 [C]Provided meaningful commit messages (about part 1 only)':1,\
'2.1 Report as a markdown file, found in doc directory':1,\
'2.2 [C]Good use of markdown e.g. headings':1,\
'2.3 [C]Describe whether you have used any of the tools or equivalent tools in the past':1,\
'2.4 [C]Describe how you think the tools new to you will change your development practice':2,\
'2.5 Report should be between 300-500 words (+10% allowed)':1,\
'2.6 [C]Git: committed and provided meaningful commit messages (about part 2 only)':1,\
'3.1 [C]Updated README.md':1,\
'3.2 [C]Included comments in code (e.g. referenced external code)':1,\
'3.3 a) Argument Implementation (2 marks, 0.5 per option)':2,\
'3.4 [C]A Multi-Media experience (1 mark)':1,\
'3.5 [C]Git: committed and provided meaningful commit messages (about part 3 only)':1,\
'4 DO NOT SUBMIT INCORRECT FILES (e.g. venv)':0}

def create_parser():
    """
    Creates an argument parser for the script.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Process directory paths and API key for the marking system.")

    # Adding arguments to the parser
    parser.add_argument(
        '--root_dir', 
        type=str, 
        default='./Raw', 
        help='Root directory for raw submissions (default: ./Raw)'
    )
    
    parser.add_argument(
        '--markdown_dir', 
        type=str, 
        default='./MarkDowns', 
        help='Directory to save markdown reports (default: ./MarkDowns)'
    )
    
    parser.add_argument(
        '--prompts_dir', 
        type=str, 
        default='./prompts', 
        help='Directory containing prompt files (default: ./prompts)'
    )
    
    parser.add_argument(
        '--output_dir', 
        type=str, 
        default='.', 
        help='Output directory for generated files (default: .)'
    )

    parser.add_argument(
        '--marking_table', 
        type=str, 
        default='./marking.xlsx', 
        help='Path of the marking table (default: ./marking.xlsx)'
    )

    parser.add_argument(
        '--apikey', 
        type=str, 
        default=None, 
        help='API key for external services (default: None)'
    )

    return parser

def check(args):
    """
    Checks the existence of necessary files and directories, as well as the API key validity.

    Args:
        args: The parsed command-line arguments.

    Raises:
        SystemExit: If any of the checks fail.
    """
    # Check for necessary prompt files
    prompt_files = ['CODE.txt', 'GitM.txt', 'PANDA.txt', 'REPORT.txt', 'MarkdownReport.txt']
    missing_files = [file for file in prompt_files if not os.path.isfile(os.path.join(args.prompts_dir, file))]

    if missing_files:
        print(f"Error: The following required prompt files are missing in '{args.prompts_dir}': {', '.join(missing_files)}")
        sys.exit(1)

    # Check if markdown_dir exists, if not, create it
    if not os.path.exists(args.markdown_dir):
        os.makedirs(args.markdown_dir)
        print(f"Created directory: {args.markdown_dir}")

    # Check if output_dir exists, if not, create it
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created directory: {args.output_dir}")

    # Check if APIkey.txt exists and is not empty
    api_key_file = os.path.join(args.prompts_dir, 'APIkey.txt')
    if os.path.isfile(api_key_file):
        with open(api_key_file, 'r') as f:
            api_key_content = f.read().strip()
            if api_key_content == '':
                print("Warning: APIkey.txt is empty.")
                if args.apikey is None or args.apikey.strip() == '':
                    print("Error: API key is missing. Please provide an API key either in APIkey.txt or as a command-line argument.")
                    sys.exit(1)
    else:
        print(f"Warning: APIkey.txt not found in '{args.prompts_dir}'. Relying on the provided API key.")

        if args.apikey is None or args.apikey.strip() == '':
            print("Error: API key is missing. Please provide a valid API key.")
            sys.exit(1)