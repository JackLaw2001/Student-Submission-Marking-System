import os
import re
from glob import glob
import openai
import zipfile as zf
import tarfile as tf
import rarfile as rf

class GPTMarker:
    def __init__(self, prompt, fullmark, chatmodel = "gpt-4o"):
        """
        Initializes the GPTMarker with maximum scores and the prompt.

        Args:
            prompt (str): The initial prompt message to send to the ChatGPT model.
            fullmark (list): A list of maximum scores for each criterion.
        """
        self.prompt = prompt
        self.fullmark = fullmark
        self.chatmodel = chatmodel

    def __call__(self, message):
        """
        Enables the GPTMarker instance to be called as a function and processes the grading.

        Args:
            message (str): The message or query for which ChatGPT will provide a score.

        Returns:
            list: A list of integer scores for each evaluation criterion.
        """
        while True:
            # Send a request to OpenAI's chat completion API
            response = openai.chat.completions.create(
                model=self.chatmodel,
                messages=[
                    {"role": "system", "content": "You are an teaching assistant grading for the Programming Portfolio 1 course."},
                    {"role": "user", "content": self.prompt.format(**message)}
                ]
            )
            # Parse the response to get the scores as a list
            reply = response.choices[0].message.content.strip().split(',')
            print('ChatGPT is marking: {}; Full mark: {}'.format(response.choices[0].message.content.strip(), self.fullmark))
            
            # Verify if the response has the expected number of scores
            if len(reply) == len(self.fullmark):
                is_valid = True  # Flag to check if all scores are valid
                for i in range(len(self.fullmark)):
                    if reply[i].isdigit() and int(reply[i]) <= self.fullmark[i]:
                        reply[i] = int(reply[i])  # Convert valid scores to integers
                    else:
                        is_valid = False  # Set flag to False if any score is invalid
                        break
                if is_valid:
                    break  # Exit the loop if all scores are valid
        return reply


def read_text_file(file_path):
    """
    Reads the entire content of a text file and returns it as a string.
    
    Parameters:
    file_path (str): The path to the text file.

    Returns:
    str: The contents of the file as a single string, or None if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Read the entire file content
        return content
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")  # Handle file not found error
        return None
    except IOError:
        print(f"Error: Could not read the file at '{file_path}'.")  # Handle IO errors
        return None

def save_txt_file(content, file_path):
    """
    Saves the provided text content to a specified file.

    Parameters:
        content (str): The text content to save.
        file_path (str): The path where the text file will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)  # Write the text content to the file    
        
def extract_file(file_path, extract_to=None):
    """
    Automatically identifies the type of compressed file and extracts it to the directory of the compressed file
    or to a new folder named after the file in the same directory.
    
    Parameters:
        file_path (str): The path to the compressed file.
        extract_to (str): The target path for extraction. If not specified:
            - zip files are extracted to their current directory;
            - tar and rar files create a subdirectory named after the file in the current directory.
    
    Supported file formats:
        - zip
        - tar, tar.gz, tar.bz2
        - rar (requires the `rarfile` module)
    
    Returns:
        bool: Whether the extraction was successful.
    """
    if not os.path.isfile(file_path):
        print(f"{file_path} is not a valid file path.")
        return False

    # Get the directory of the file and the file name without extension
    file_dir = os.path.dirname(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Set the default extraction directory if extract_to is not specified
    if extract_to is None:
        # .zip files are extracted to the directory of the file
        if file_path.endswith('.zip'):
            extract_to = file_dir
        # .tar and .rar files are extracted to a subdirectory named after the file
        elif file_path.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz', '.rar')):
            extract_to = os.path.join(file_dir, file_name)
            # Create the subdirectory if it does not exist
            if not os.path.exists(extract_to):
                os.makedirs(extract_to)
        else:
            print(f"Unsupported file format: {file_path}")
            return False
    
    # Choose extraction method based on file extension
    try:
        if file_path.endswith('.zip'):
            with zf.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif file_path.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz')):
            with tf.open(file_path, 'r:*') as tar_ref:
                tar_ref.extractall(extract_to)
        elif file_path.endswith('.rar'):
            with rf.RarFile(file_path, 'r') as rar_ref:
                rar_ref.extractall(extract_to)
        else:
            print(f"Unsupported file format: {file_path}")
            return False
        print(f"Extraction successful: {file_path} -> {extract_to}")
        return True
    except Exception as e:
        print(f"Extraction failed: {e}")
        return False
        
def merge_markdown_files(folder_path, output_file):
    """
    Merges all .md files in the specified folder into a single markdown file.

    Parameters:
        folder_path (str): The path to the folder containing .md files.
        output_file (str): The path where the merged markdown file will be saved.
    """
    # Find all .md files in the specified folder, sorted by filename
    md_files = sorted(glob(os.path.join(folder_path, '*.md')))
    
    # Open the output file for writing
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as infile:
                # Write the content of each file to the output file
                outfile.write(infile.read())
                outfile.write('\n\n')  # Add two newlines for spacing between files

    print(f"Merged {len(md_files)} markdown files into '{output_file}'.")
    
def count_files_in_directory(folder_path):
    """
    Counts the total number of files in the specified directory.

    Parameters:
        folder_path (str): The path to the folder to count files in.

    Returns:
        int: The total number of files in the directory.
    """
    total_files = 0

    # Loop through all items in the directory
    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)  # Add the number of files in the current directory

    return total_files
    
def find_files_with_suffix(suffix, search_path='.'):
    """
    Finds files with a specified suffix and returns their paths.
    
    Parameters:
        suffix (str): The file suffix to search for (e.g., '.txt').
        search_path (str): The directory path to search, defaults to the current directory.
        
    Returns:
        list: A list containing the paths of all matching files.
    """
    # Use glob to find files with the specified suffix, supports recursive search
    pattern = os.path.join(search_path, '**', f'*{suffix}')
    matching_files = glob(pattern, recursive=True)  # Search for matching files
    
    return matching_files

def parse_student_info(file_path):
    """
    Parses student information from a specified file and extracts relevant details.
    
    Parameters:
        file_path (str): The path to the file containing student information.
        
    Returns:
        dict: A dictionary containing the student's Name, ID, Email, and Tutor, or None if not found.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines from the file

    # Use regular expressions to extract information
    name_match = re.search(r'^(.*?)(?=\s\(\d{9}\))', lines[0])  # Match name up to student ID
    id_match = re.search(r'\((\d{9})\)', lines[0])  # Extract student ID
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', lines[1])  # Extract email
    tutor_match = re.search(r'Tutor:\s(.+)', lines[2])  # Extract tutor information

    # Extract each field, returning None if not found
    name = name_match.group(1).strip() if name_match else None  # Remove leading/trailing whitespace
    student_id = id_match.group(1) if id_match else None
    email = email_match.group() if email_match else None
    tutor = tutor_match.group(1) if tutor_match else None

    return {
        'Name': name,
        'ID': student_id,
        'Email': email,
        'Tutor': tutor
    }

def extract_commit_info(head_path):
    """
    Reads commit information from the .git/HEAD file and extracts 'commit: xxx' format records.

    Parameters:
        head_path (str): The path to the .git/HEAD file.

    Returns:
        list: A list of commit information records that match the criteria.
    """
    commit_messages = []
    
    # Read the content of the HEAD file
    with open(head_path, 'r') as file:
        head_content = file.read()  # Read the entire content

    # Use regular expressions to extract records in the 'commit: xxx' format
    matches = re.findall(r'\b(commit: .+)', head_content)  # Find all matches for commit records
    
    # Add all found matches to the list
    commit_messages.extend(matches)

    return commit_messages

def get_directory_structure(root_dir):
    """
    Generates a string representation of the directory structure starting from the specified root directory.

    Parameters:
        root_dir (str): The root directory to traverse.

    Returns:
        str: A formatted string representing the directory structure.
    """
    structure = []  # List to hold the directory structure

    def traverse(directory, prefix=""):
        # Get all non-hidden files and folders in the current directory
        items = [item for item in os.listdir(directory) if (not item.startswith('.')) and ('venv' not in item)]
        # Iterate over the list of items and display structure
        for index, item in enumerate(items):
            path = os.path.join(directory, item)
            # Determine if the current item is the last one
            is_last = (index == len(items) - 1)
            # Use different prefixes based on whether the item is the last
            if is_last:
                structure.append(f"{prefix}└── {item}  ")  # Last item
                next_prefix = prefix + "    "
            else:
                structure.append(f"{prefix}├── {item}  ")  # Not the last item
                next_prefix = prefix + "│   "
            # Recursively traverse if the item is a directory
            if os.path.isdir(path):
                traverse(path, next_prefix)

    traverse(root_dir)  # Start traversing from the root directory
    # Join the structure list with newlines to create the final structure string
    return "\n".join(structure)

def generate_markdown_report_string(marking, full_marking, studinfo, assinfo, dirn):
    """
    Generates a Markdown formatted report based on the marking information.

    Parameters:
        marking (dict): A dictionary containing the scores for each marking point.
        full_marking (dict): A dictionary containing the full scores for each marking point.
        studinfo (dict): A dictionary containing student information.
        assinfo (dict): A dictionary containing assignment information.
        dirn (str): The directory path to include in the report.

    Returns:
        str: A Markdown formatted string representing the marking report.
    """
    # Start with the report title
    markdown_content = ""
    # Iterate through the dictionary to generate the marking report
    for point in marking:
        score = marking[point]
        full_score = full_marking[point]
        
        if score < full_score:
            markdown_content += f"{point}: **{score}** / {full_score}  \n"  # Highlight scores below full marks
        else:
            markdown_content += f"{point}: {score} / {full_score}  \n"  # Normal display for full marks

    return markdown_content