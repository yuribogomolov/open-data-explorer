from open_data_explorer.queries.query_runner import QueryRunner


def test_query_runner():
    runner = QueryRunner()
    model = runner.search('NYC population')
    print(model)
