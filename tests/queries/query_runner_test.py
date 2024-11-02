from open_data_explorer.queries.query_runner import QueryRunner


def test_query_runner():
    runner = QueryRunner()
    resources = runner.select_datasets('washington road accidents')
    for resource in resources:
        print(resource)
