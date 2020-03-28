import datetime
from functools import reduce
import argparse
import sys

F_OFFSET = [num for num in range(1,10) if not num % 2 == 1] 
M_OFFSET = [num for num in range(1,10) if num % 2 == 1] 

PPL_OFFSET = ["{:03d}".format(num) for num in range(1,301)]

VALLIDATE_OFFSET = [num for num in range(1,10)]

governorates = {
        "alexandria":2,
        "aswan":28,
        "asyut":25,
        "beheira ":18,
        "beni suef":22,
        "cairo":1,
        "dakahlia":12,
        "damietta":11,
        "faiyum":23,
        "gharbia":16,
        "giza":21,
        "ismailia":19,
        "kafr el sheikh":15,
        "luxor":29,
        "matruh":33,
        "minya":24,
        "monufia":17,
        "new valley":32,
        "north sinai":34,
        "port said":03,
        "qalyubia":14,
        "qena":27,
        "red sea":31,
        "sharqia":13,
        "sohag":26,
        "south sinai":35,
        "suez":04,
}

def get_governorate(te):
    if str(te).lower() in governorates.keys():
        return governorates[te]
    else:
        print("governorates not found allowed values {}".format(str(governorates.keys())))
        exit(0)

def year_offset(before_2000=False):
    return int(2) if before_2000 else int(3)

def add_offset(p,offset):
    return ["{}{}".format(p,of) for of in offset]

def generate_data(start_i="", end_i="", ct_code="cairo", gender="f"):
    data = []
    fnum = 2
    ctcode = get_governorate(ct_code)
    try:
        yee = int(str(start_i).split('-')[2])
        fnum = 2 if yee < 2000 else 3
    except Exception as e:
        print("wrong format")
        exit(0)
    def get_time(input):
        try:
            return datetime.datetime.strptime(input, "%d-%m-%Y")
        except Exception as e:
            print("Wrong date format please enter smt like 01-01-1997")
            exit(0)
    start = get_time(start_i)
    end = get_time(end_i)
    days_generated = [(start + datetime.timedelta(days=x)).strftime("{}%y%m%d{:02d}".format(fnum,ctcode)) 
    for x in range(0, (end-start).days)]
    for day in days_generated:
        stg = add_offset(day,PPL_OFFSET)
        stg2 = []
        add_gender = lambda e : stg2.append(add_offset(e, M_OFFSET if not gender == "F".lower() else F_OFFSET))
        list(map(add_gender,stg))
        to_addval = reduce(lambda x,y: x+y, stg2)
        stg3 = []
        add_validate = lambda e : stg3.append(add_offset(e,VALLIDATE_OFFSET))
        list(map(add_validate,to_addval))
        data+= reduce(lambda x,y: x+y, stg3)
    return data





# Process command-line arguments.
if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help = True, description = "Generating egyptian national identity number "
                                  "for testing how government public services could be abused")

    parser.add_argument('-city', action='store', default='cairo', help='the city you want to generate IDs for'
                                                                               ' (default cairo)')
    parser.add_argument('-outputfile', action='store',default='output.txt',
                        help='Output filename to write generated numbers')

    group = parser.add_argument_group('info')

    group.add_argument('-start', action='store',required=True,  help='Start date ex: 01-08-1999 ')
    group.add_argument('-end', action='store',required=True,  help='End date ex: 01-08-1999 ')
    group.add_argument('-gender', action='store', default='F', help='target gender , F for female and M for male ')

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    options = parser.parse_args()
    print("Generating Data Please Wait ...")
    data = generate_data(start_i=str(options.start),end_i=str(options.end),gender=str(options.gender),ct_code=str(options.city))

    if options.outputfile:
        print("writing to {}".format(options.outputfile))
        with open(options.outputfile, 'w') as f:
            for item in data:
                f.write("%s\n" % item)