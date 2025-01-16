# Knit2PDF

This is a CLI tool that allows you to generate a PDF of a knitting / crocheting pattern based off a youtube video.

## Installation
1. Clone the repository
- `git clone https://github.com/sarasoh1/knit2pdf`

2. Activate poetry
- `poetry shell`
- `poetry install`

3. Create the folders
- `/videos/`
- `/transcripts/`
- `/patterns/`

4. Now it's ready for use!
- `knit2pdf "[youtube_link]"`

Add video language if the language isn't english.
`knit2pdf "[youtube_link]" --language kr`
