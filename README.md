# MangaReader
Manga reading client and configurable downloader in Python

# How To Use
In your terminal,
  ```bash
  git clone github.com/alphactory/mangareader
  pip install -r requirements.txt
  ```
Edit config.yaml with the asked fields for an online comic whose images are iterable (i.e. domain/path/1.jpg, 2.jpg, etc) and run 
  ```bash
  python3 comic_reader.py
  ```

# Controls for viewer
    j to jump to a new page
    Escape to exit
    lefty:
        Move forward a page
            a or s
        Move back a page
            w or d
        Adjust forward
            q
        Adjust back
            e
    righty:
        Move forward a page
            Left or Down
        Move back a page
            Right or Up
        Adjust forward
            Comma
        Adjust back
            Period
