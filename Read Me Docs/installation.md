# Check Python versions installed

`py -0 versions`

Download Python 3.11 from the official website and install it
Once downloaded, follow the installation instructions for your operating system

# Create a virtual environment with Python 3.11
`python3.11 -m venv venv`

# Activate the virtual environment
## On Windows:
`venv\Scripts\activate`
## On macOS/Linux:
`source venv/bin/activate`

# Install the dlib.whl file
`pip install ./installation/dlib.whl`

# Install the dependencies from requirements.txt
`pip install -r ./installation/requirements.txt`

# Run the Flask application
`python app.py`
