import sqlite3
import os
import random
import csv

CHUNK_SIZE = 300
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORY_PATH = os.path.join(CURR_DIR, 'categories.csv')
CLUE_PATH = os.path.join(CURR_DIR, 'clues')

DB = sqlite3.connect('clues.db')

def clues_file_name(category_id):
    return os.path.join(CLUE_PATH, '{}.csv'.format(category_id))

def query_db(query, args=(), one=False):
    cur = DB.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def write_categories():
    sql = """SELECT
          categories.id as category_id,
          categories.category,
          COUNT(*) AS cnt
        FROM
          categories
          INNER JOIN classifications
            ON categories.id = classifications.category_id
          INNER JOIN clues
            ON clues.id = classifications.clue_id
        GROUP BY 1,2"""
    res = query_db(sql)
    new_res = []
    for category in res:
        new_res += [category] * int((category[2] / 5) + 0.5)
    with open(CATEGORY_PATH, 'w') as outfile:
        writer = csv.writer(outfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
        _ = writer.writerow(['category_id', 'category', 'cnt'])
        for row in new_res:
            _ = writer.writerow(row)

def write_clues():
    sql = """SELECT
        classifications.category_id,
        clues.round,
        clues.value,
        documents.clue,
        documents.answer,
        categories.category,
        airdates.airdate
      FROM
        documents
        INNER JOIN clues
          ON documents.id = clues.id
        INNER JOIN classifications
          ON clues.id = classifications.clue_id
        INNER JOIN categories
          ON classifications.category_id = categories.id
        INNER JOIN airdates
          ON clues.game = airdates.game
      ORDER BY classifications.category_id
        """
    res = query_db(sql)
    for row in res:
        file_name = clues_file_name(row[0])
        if os.path.exists(file_name):
            with open(file_name, 'a') as outfile:
                writer = csv.writer(outfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
                _ = writer.writerow(row)
        else:
            with open(file_name, 'w') as outfile:
                writer = csv.writer(outfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
                _ = writer.writerow(['category_id','round','value','clue','answer','category','airdate'])
                _ = writer.writerow(row)


def pick_next_random_line(file, offset, chunk_size=CHUNK_SIZE):
    file.seek(offset)
    chunk = file.read(CHUNK_SIZE)
    lines = chunk.split(os.linesep)
    line_offset = offset + len(os.linesep) + chunk.find(os.linesep)
    return line_offset, lines[1]

def get_n_random_lines(path, n=5):
    length = os.stat(path).st_size
    results = []
    result_offsets = set()
    with open(path) as input:
        header = input.readline().strip()
        for x in range(n):
            while True:
                offset, line = pick_next_random_line(input, random.randint(0, length - CHUNK_SIZE))
                if not offset in result_offsets:
                    result_offsets.add(offset)
                    results.append(line)
                    break
    return list(csv.DictReader(results, fieldnames=header.split('|'), delimiter='|', quoting=csv.QUOTE_MINIMAL))

def get_clues_from_cat(category_id):
    """Picks one random game from the category"""
    with open(clues_file_name(category_id)) as f:
        data = list(csv.DictReader(f, delimiter='|', quoting=csv.QUOTE_MINIMAL))
    airdate = random.choice(list(set([d['airdate'] for d in data])))
    return [d for d in data if d['airdate'] == airdate]


if __name__ == '__main__':
    #write_categories()
    #write_clues()
    print(get_n_random_lines(CATEGORY_PATH))
    print(get_clues_from_cat(100036))
