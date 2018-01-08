

class TestCases:

    def test_init(self, testapp):
        request_data = {}
        response = testapp.get(
            path='/',
            content_type='application/json',
            data=request_data
        )

        print()
