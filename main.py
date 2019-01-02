import argparse
import datetime
import json
import os


class Record:
    def __init__(self, msg: str, date: datetime.datetime = datetime.datetime.now(), rec_id=0):
        self.date = date
        self.msg = msg
        self.id = rec_id


class DB:
    def __init__(self, db_file: str):
        self.db_file = db_file

        if not os.path.isfile(self.db_file):
            with open(self.db_file, "w") as js_file:
                js_file.write('{"db":{}}')
        with open(self.db_file, "r") as js_file:
            self.js_data = json.load(js_file)

    def _dump(self):
        with open(self.db_file, "w") as js_file:
            json.dump(self.js_data, js_file)

    def save(self, record: Record):
        if self.js_data["db"].keys():
            rec_id = int(max(self.js_data["db"].keys())) + 1
        else:
            rec_id = 1
        record.id = rec_id
        self.js_data["db"][str(rec_id)] = {"msg": record.msg, "date": str(record.date)}
        self._dump()

    def loads(self):
        out_recs = []
        db_js = self.js_data["db"]
        for rec_js in db_js:
            out_recs.append(Record(db_js[rec_js]["msg"], db_js[rec_js]["date"], int(rec_js)))
        return out_recs

    def load(self, rec_id: int):
        rec_js = self.js_data["db"][str(rec_id)]
        return Record(rec_js["msg"], rec_js["date"], rec_id)

    def update(self, record: Record):
        db_js = self.js_data["db"]
        del db_js[str(record.id)]
        db_js[str(record.id)] = {"msg": record.msg, "date": str(record.date)}
        self._dump()

    def print_records(self):
        recs = sorted(self.loads(), key=lambda r: r.id)
        for record in recs:
            print(record.id, record.date, record.msg)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", type=str, help='add', default='')
    parser.add_argument("-l", "--list", action='store_true')
    parser.add_argument("-u", "--update", nargs=2)
    return parser.parse_args()


def main():
    db = DB("test.json")
    args = parse_args()

    if args.list:
        db.print_records()
    elif args.add:
        db.save(Record(args.add))
    elif args.update:
        record = db.load(args.update[0])
        record.msg = args.update[1]
        db.update(record)


if __name__ == "__main__":
    main()
