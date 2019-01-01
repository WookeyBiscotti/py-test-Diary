import os
import json
import datetime
import argparse


class Record:
    def __init__(self, msg: str, date: datetime.datetime = datetime.datetime.now()):
        self.date = date
        self.msg = msg


class DB:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def save(self, record: Record):
        db_js = self._load_js()
        if db_js["db"].keys():
            rec_id = int(max(db_js["db"].keys())) + 1
        else:
            rec_id = 1
        db_js["db"][str(rec_id)] = {"msg": record.msg, "date": str(record.date)}
        self._save_js(db_js)

    def _load_js(self):
        if not os.path.isfile(self.db_file):
            with open(self.db_file, "w") as js_file:
                js_file.write('{"db":{}}')

        with open(self.db_file, "r") as js_file:
            return json.load(js_file)

    def _save_js(self, db_js):
        with open(self.db_file, "w") as js_file:
            json.dump(db_js, js_file)

    def load(self):
        out_recs = []
        db_js = self._load_js()["db"]
        for rec_js in db_js:
            out_recs.append(Record(db_js[rec_js]["msg"], db_js[rec_js]["date"]))
        return out_recs

    def print_records(self):
        for record in self.load():
            print(record.date, record.msg)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", type=str, help='add', default='')
    parser.add_argument("-l", "--list", action='store_true')
    return parser.parse_args()


def main():
    db = DB("test.json")
    args = parse_args()

    if args.list:
        db.print_records()
    elif args.add:
        db.save(Record(args.add))


if __name__ == "__main__":
    main()
