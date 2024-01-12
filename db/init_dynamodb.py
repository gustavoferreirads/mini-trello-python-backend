import yaml

from dynamodb_config import get_dynamodb_resource

dynamodb = get_dynamodb_resource()


def create_tables(config_file):
    with open(config_file, 'r') as file:
        tables = yaml.safe_load(file)

    for table_name, properties in tables.items():
        print(f"Creating table {table_name}...")
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=properties['KeySchema'],
            AttributeDefinitions=properties['AttributeDefinitions'],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )


if __name__ == "__main__":
    create_tables('migration/dynamodb_tables.yaml')
