# Project Mashup

A web application that allows you to download and convert videos to audio, trim the audio, and merge the trimmed audios into one file. The resulting audio file can be sent to an email address of your choice.

## Features
- A form with the following input boxes:
  - Keyword (for the singer's name)
  - Number of downloads (number of videos to be downloaded and converted to audio)
  - Duration time (to trim the audio obtained)
- Submit button that sends the merged audio file to the email address entered in the form

## Requirements
- Python 3
- A web browser

## Installation
1. Clone or download this repository.
2. Install the required packages using the following command:
```console
virtualenv -p python3 venv source
venv/bin/activate
pip install -r requirements.txt
```

## Usage
1. Run the application using the following command:
```console
python manage.py migrate
python manage.py runserver

```
2. Open a web browser and go to `http://127.0.0.1:8000/`.
3. Fill in the form with the keyword, number of downloads, and duration of each audio file.
4. Click the submit button to receive the merged audio file in your email.

![Sample](/sample.jpg)

## Contribution
Feel free to contribute to this project by submitting a pull request.

