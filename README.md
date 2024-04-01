# rechord

The plan is:

Step 1: Get your listening stats.

Step 2: Generate a best-of list of albums.

Step 3: Generate a shopping list from discogs.

## Get Started

### Authenticate with Last.fm

```bash
python get_session.py \
    --api-key [API-KEY] \
    --secret [SECRET]
```

Follow the instructions to get a session key. You will need it for the next step.

### Download your listening stats

```bash
python download_tracks.py \
    --api-key [API-KEY] \
    --secret [SECRET] \
    --session [SESSION] \
    --user [USER] \
    --from [FROM-YYYY-MM-DD] \
    --to [TO-YYYY-MM-DD] \
    --dest-dir [DEST-DIR]
```

This will download your data in several JSON files to the destination directory.

