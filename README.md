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

## Usage

1. **Clone the Repository** (if applicable):
   
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   
2. **Install Dependencies** : Make sure to install the required Python packages:
   
   ```bash
   pip install -r requirements.txt
   
3. **Run the Script**: Execute the script from the command line. The following command-line arguments are available:
   
   ```bash
   python marking_script.py --root_dir <path_to_raw_submissions> --markdown_dir <path_to_save_markdown_reports> --prompts_dir <path_to_prompts> --output_dir <output_directory> --apikey <your_api_key>
   ```
   
   - `--root_dir`: Root directory for raw submissions (default: ./Raw)
   - `--markdown_dir`: Directory to save markdown reports (default: ./MarkDowns)
   - `--prompts_dir`: Directory containing prompt files (default: ./prompts)
   - `--output_dir`: Output directory for generated files (default: .)
   - `--apikey`: API key for ChatGPT (default: None)

## Example
   ```bash
   python marking_script.py --root_dir ./Raw --markdown_dir ./MarkDowns --prompts_dir ./prompts --apikey YOUR_API_KEY

