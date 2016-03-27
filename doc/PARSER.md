# Parser

Reads html files and converts them to somehow structured JSON with parsed contents.

## Output Fields

- type (one out of author, conference and journal)
- title (Which functions for name of authors as well)
- isbn (empty if non existent)
- content
- uuid (how to find unique IDs, or hash the content of file)

### Content

content is just a string of parsed words (lower cased) seperated by spaces.

Test:

"Hola WHATS-up" -> "hola whats up"

## Output

Folder named parsed with subfolders conference, author and journal. Filename is UUID.json
