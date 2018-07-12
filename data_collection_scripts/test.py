from google.cloud import bigquery
from formatted_string import formatted_name
import os, sys, csv, inspect


def table_query(input_A):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        "C:\\Users\dorel.moran\PycharmProjects\csv_scripts\BigQuery\google_key_credentials.json"
    #TODO;: put file in GIT repository

    client = bigquery.Client()
    dataset_id = 'tests'
    dataset_ref = client.dataset(dataset_id)
    table_id = 'test3'
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)

    query = insert_query(input_A, table)
    print(query + '\n')

    query_job = client.query(query)
    print('Insert query finished successfuly.')

def insert_query(input_A, table):
    with open(input_A + '.csv', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        input_list = []
        input_list_sql = ''
        #print(reader.__next__())   # print out the file's column names
        '''
        @col_headers --> Change the input csv column names to insert to the db.
        '''
        csv_col_headers = ['\ufeffitem_name', 'item_type', 'item_year', 'fb_annotation']
        for row in reader:
            input_list.append(["'" + row[csv_col_headers[0]] + "'", "'" + row[csv_col_headers[1]] + "'",
                               "'" + row[csv_col_headers[2]] + "'", "'" + row[csv_col_headers[3]] + "'",
                               'CURRENT_TIMESTAMP'])
        for i in range(len(input_list)):
            input_list_sql += '(' + ','.join(input_list[i]) + '),'
            if input_list[i] == input_list[-1]:
                input_list_sql = input_list_sql[:-1]
        '''
    `   @db_col_headers --> Change column names here based on the databse columns to add values for.
        '''
        db_col_headers = ['item_name', 'item_type', 'item_year', 'fb_annotation', 'item_timestamp']
        original_db_col_headers = []
        for i in range(len(table.schema)):
            original_db_col_headers.append(table.schema[i].name)
        for i in range(len(db_col_headers)):
            if db_col_headers[i] not in original_db_col_headers:
                original_schema = table.schema
                new_schema = original_schema[:]
                new_schema.append(bigquery.SchemaField(db_col_headers[i], 'STRING'))
                table.schema = new_schema
                table = bigquery.Client().update_table(table, ['schema'])
                print('Added new column:', db_col_headers[i])
        db_col_headers_sql = '('
        for i in range(len(db_col_headers)):
            db_col_headers_sql += db_col_headers[i] + ','
            if db_col_headers[i] == db_col_headers[-1]:
                db_col_headers_sql = db_col_headers_sql[:-1] + ')'
        return ('\nINSERT INTO ' + table.dataset_id + '.' + table.table_id + db_col_headers_sql +
                ' VALUES ' + input_list_sql)


def main():
    input_A = sys.argv[1]
    table_query(input_A)

if __name__ == '__main__':
    main()