# Grading Tools

Welcome to my setup as an SLI (Student Lab Instructor), essentially a TA, to grade my student's labs! Obviously, this
repository is tailored to my specific grading habits and needs, but I feel like it might be nice to have as a starting
point for anyone new to grading!

## Setup
To start, you can grab this repository using
```
git clone https://github.com/thecreatorguy/gradingtools.git
cd gradingtools
```

Now that the first step is complete, you'll want to check out [gradefast](https://github.com/jhartz/gradefast). This
is an excellent tool that I use to grade labs quickly, executing commands for each lab. To install it, you'll want
to set up a virtual environment for python. I've found that `python 3.7`, the most recent version when I started grading,
did not work with gradefast, so I would recommend `python 3.6`.
```
python3 -m venv venv

venv\Scripts\activate    # If on Windows
source venv/bin/activate # If not on Windows (this is what I use)

pip install -r requirements.txt
```

This will initialize your virtual environment. Now to install gradefast:
```
git clone https://github.com/jhartz/gradefast.git
cd gradefast
git submodule update --init
```

The last thing to download will be the [chromedriver executable](https://chromedriver.chromium.org/). This is used in
the `submit_grades.py` script to upload the grades from gradefast to MyCourses, RIT's online resource for courses. Put
this in the top level directory, `gradingtools/`.

Finally, you should copy the `.env.example` as `.env` and make your changes there using the table below.

Setup is complete!

### .env
| Variable | Description |
| ---:| --- |
| `GRADINGTOOLS_DIRECTORIES` | Directories for grading scripts to ignore when looking for grading roots |
| `GRADEFAST_SHELL_PATH` | Shell that you want gradefast to execute commands with |
| `MYCOURSES_USERNAME/PASSWORD` | Self explanatory- used for automatic entry of username and password in MyCourses |
| `GRADE_SHEET_URL` | The exact url of the grade entry sheet for the course- includes all labs, exams, etc |

## Usage

### Grading
For each zip of submissions downloaded from MyCourses, extract this into a folder within the grading root. If you want
the semi-automatic uploading of grades to MyCourses, name this the same as the header in the grading sheet page that
it corresponds to, spacing and capitalization don't matter.

The main script is `grade.py`. From within the virtual environment, run `python3 grade.py`. This will set up the folder
that you choose, moving all files to folders that gradefast will recognize, renaming the files from the strange format
that MyCourses uses to the correct format, with the name of the student being the upper directory. If the file that
was uploaded was a `.zip` file, the zip will be extracted. `index.html` will be removed, acting as the flag for
completed operations. Finally, the template from the `provided/` folder will be copied in- make your changes here,
according to the gradefast wiki. If you would like to change the template for most commonly used setups, feel free
to do so.

If you have any folder named the same as your grading root in `provided/`, then the contents of that folder will be
copied into *each* submission folder- this is very helpful for automatically running grading/testing scripts, because
gradefast runs commands from within each folder.

After the setup is complete, gradefast will be run with the proper arguments.

### Automatic Grade Submission
From within the virtual environment, run `python3 submit_grades.py`. After you select which folder to upload, the grades
will be submitted on MyCourses before your very eyes!

Unfortunately, this feature is not yet complete- some rows are skipped in the upload process, so you still have to
input approximately 1/4 of the grades manually.

#### Todo:
1. Comment `grade.py` and `submit_grades.py`
