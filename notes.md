# Jop

## Pages

- Picking a category
- Showing clues
- MVP: Show you random categories, then it picks a random set of game clues for a random game?
- Process for clues:
  - Show buttons for unseen in category
  - Click the button and it shows
    - Clue
    - Countdown timer
    - button to say "I guessed"
    - Click button to say "I guessed", or timer runs out:
      - Record question as seen
      - Show answer
      - Show button for "I got it!" and "I ain't got it!"
      - Click on either button to go back to unseen screen

- Create a little app that'll pick a category, and spit out questions randomly with that category?
- Record right/wrong (5 second limit)





SELECT
  clues.id,
  clues.game,
  clues.round,
  clues.value,
  documents.clue,
  documents.answer,
  categories.category
FROM
  documents
  INNER JOIN clues
    ON documents.id = clues.id
  INNER JOIN classifications
    ON clues.id = classifications.clue_id
  INNER JOIN categories
    ON classifications.category_id = categories.id
WHERE
  classifications.category_id = ?

airdates
  game INTEGER PRIMARY KEY,
  airdate TEXT
documents
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  clue TEXT,
  answer TEXT
categories
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT UNIQUE
clues
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  game INTEGER,
  round INTEGER,
  value INTEGER,
  FOREIGN KEY(id) REFERENCES documents(id),
  FOREIGN KEY(game) REFERENCES airdates(game)
classifications
  clue_id INTEGER,
  category_id INTEGER,
  FOREIGN KEY(clue_id) REFERENCES clues(id),
  FOREIGN KEY(category_id) REFERENCES categories(id)

SELECT
  categories.category,
  COUNT(*) AS cnt
FROM
  categories
  INNER JOIN classifications
    ON categories.id = classifications.category_id
  INNER JOIN clues
    ON clues.id = classifications.clue_id
GROUP BY 1
ORDER BY 2 DESC;
