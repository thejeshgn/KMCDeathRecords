import os
import hjson
import dataset

db = dataset.connect('sqlite:///./data/death_records.sqlite')
table = db["death_records"]

RECORDS_SOURCE = "kmcgov.in"
RECORDS_CITY = "Kolkata"

raw_data_folder = "./raw"
raw_data_file_name = "./raw/{file_name}"

def get_data_files():
    l = os.listdir(raw_data_folder)
    l.sort()
    return l

    
def process_file(file_name):
    print("Processing {file_name}".format(file_name=file_name))
    source_raw_data_file_path = raw_data_file_name.format(file_name=file_name)


    file_obj = open(source_raw_data_file_path, "r")    
    file_data = file_obj.read()
    file_obj.close()
    recordsDateOfDeath = file_name.replace(".json","")

    data = hjson.loads(file_data)
    insert_array = []
    for deathRecord in data["deathRecords"]:

        # Add extra attributes for our reference
        deathRecord["recordsSource"] = RECORDS_SOURCE
        deathRecord["recordsCity"] = RECORDS_CITY
        deathRecord["recordsDateOfDeath"] = recordsDateOfDeath
        deathRecord["recordsSourceRawDataFile"] = source_raw_data_file_path
        print(deathRecord)
        insert_array.append(deathRecord)

    table.insert_many(insert_array)        


def main():
    file_list = get_data_files()
    for file_name in file_list:
        process_file(file_name)   

if __name__ == "__main__":
    main()