# ReadAny

ReadAny is an application that can read books and PDFs aloud. This README provides instructions for setting up and using the application locally.

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

## Setup Instructions

Choose one of the following methods to create a virtual environment:

### Option 1: Using venv

1. Install virtualenv:
   ```bash
   pip install virtualenv
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source env/bin/activate
     ```

### Option 2: Using Conda

1. Create a Conda environment:
   ```bash
   conda create --name readany python=3.12
   ```

2. Activate the Conda environment:
   ```bash
   conda activate readany
   ```

## Installing Dependencies

After activating your chosen environment, install the required packages:

```bash
pip install -r requirements.txt
```
