from pandas import read_csv
import dateutil.parser
import json
def get_schedule(date, batch = 'batch_a'):
    df = read_csv(batch+'.csv', delimiter = '\t')
    classes = df[df.columns[1:]].transpose().to_dict()
    #json.dump(classes,open('batch_a.json','w'))
    if get_day(date) == 6:
        return ''
    return json.dumps(classes[get_day(date)])
def get_day(date):
    d = dateutil.parser.parse(date)
    return int(d.weekday())
get_schedule('2017-04-04')
