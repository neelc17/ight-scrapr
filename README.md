# IGHT Scrapr
A Python application that gives basic analytics for Instagram hashtags. 

## Getting Started

### Clone a Copy

Clone a copy of this project with the following command:

```
git clone https://github.com/neelc17/ight-scrapr.git
```

### Prerequisites

Before running the project, install the dependences with the following command:

```
pip install -r requirements.txt
```

## Running the Program

The application is in a very basic state right now, and can be run as a simple CLI Python program.

### Create Input File

The application works by reading from an input file that contains the list of hashtags to be analyzed. Create a file called ```hashtags.txt``` in the project directory. Type in the hashtags you wish to analyze, separated by newlines as such:

```
#wildlifephotography
#wildlifepics
#videography
#filmmaking
#yankeewithnobrim
...
```

### Starting the Program

With the ```hashtags.txt``` file saved, run the program using the following command:

```
python ight-scrapr.py
```

This will start the program, scraping and analyzing each given hashtag's posts from Instagram's website (this may take a while depending on how many hashtags were given).

When completed, two files will be created: ```output.csv``` and ```output.json```. Both files will contain the total number of posts and the mean and minimum number of likes for the top posts for each hashtag, formatted as CSV and JSON, respectively.
