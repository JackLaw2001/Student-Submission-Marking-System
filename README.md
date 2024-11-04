# Student Submission Marking System

This script processes student submissions in specified directories and grades them based on predefined criteria using a marking system powered by ChatGPT. It generates markdown reports that summarize the assessment information for each student.

## Features

- Extracts information from student submission directories.
- Utilizes ChatGPT models for grading various components of the submissions.
- Generates markdown reports containing the assessment results and feedback.
- Handles markdown files for report submissions, README, and LICENSE files.
- Checks for necessary dependencies and git commit messages.

## Requirements

- Python 3.x
- `argparse`
- `pandas`
- `BeautifulSoup4`
- `markdown`
- `openpyxl`

## Usage

1. **Clone the Repository**:

   ```bash
   git clone <repository_url>
   cd <repository_directory>

2. **Install Dependencies** : Make sure to install the required Python packages:

   ```bash
   pip install -r requirements.txt

3. **Prepare submissions**: Download submissions from NESS in the following format and extract the submissions to a folder called *Raw*. In the subdirectory of *Raw*, you should see the student submissions in the format like *24XXXXXXX*.

![NESS](https://github.com/JackLaw2001/Student-Submission-Marking-System/blob/main/figs/NESS)
Move the marking sheet to the same folder of *marking.py* and rename it as *marking.xlsx*. 
After you prepare all necessary files, the folder should looks like this:

![Folder](https://github.com/JackLaw2001/Student-Submission-Marking-System/blob/main/figs/Folder)

1. **Apply for a ChatGPT API key**: Apply a ChatGPT API key and put it in the *prompts/APIkey.txt*.   

2. **Run the Script**: Execute the script from the command line. The following command-line arguments are available:

```bash
python marking_script.py --root_dir <path_to_raw_submissions> --markdown_dir <path_to_save_markdown_reports> --prompts_dir <path_to_prompts> --output_dir <output_directory> --apikey <your_api_key>
```

- `--root_dir`: Root directory for raw submissions (default: ./Raw)
- `--markdown_dir`: Directory to save markdown reports (default: ./MarkDowns)
- `--prompts_dir`: Directory containing prompt files (default: ./prompts)
- `--output_dir`: Output directory for generated files (default: .)
- `--marking_table`: Path of the marking sheet (default: ./marking.xlsx)
- `--apikey`: API key for ChatGPT (default: None)

## Example
   ```bash
   python marking.py --root_dir ./Raw --markdown_dir ./MarkDowns --prompts_dir ./prompts --apikey YOUR_API_KEY

