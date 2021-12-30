import boto3
from time import sleep

client = boto3.client('athena', 'us-east-1')
env = 'prod'
database_name = 'jay_{}'.format(env)
work_group = 'jay-{}-AthenaWorkGroup'.format(env)
config = {'OutputLocation': 's3://jay_{}_miss/athena_query/'.format(env)}

table_list = []


def drop_partition(database, tb_name):
    print("Drop Partition Started for ", database, tb_name)
    response = client.start_query_execution(
        QueryString="ALTER TABLE {}.{} DROP PARTITION (frequency='daily')".format(database, tb_name),
        WorkGroup=work_group,
        ResultConfiguration=config)
    sleep(10)
    print("Ended for drop partition for {}\n".format(tb_name), response)


def msck_repair_table(database, tb_name):
    print("MSCK REPAIR in progress : ", database, tb_name)
    response = client.start_query_execution(
        QueryString='msck repair table `{}`.`{}`'.format(database, tb_name),
        ResultConfiguration=config,
        WorkGroup=work_group)
    sleep(10)
    print("Ended for msck repair for {}\n".format(tb_name), response)


for table in table_list:
    drop_partition(database_name, table)
    msck_repair_table(database_name, table)
