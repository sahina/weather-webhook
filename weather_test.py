from weather import simplify_date, url_for_city


def test_simplify_date():
    long_date = "2019-10-01T12: 00: 00-04: 00"
    expected = "2019-10-01"
    simple_date = simplify_date(long_date)

    assert simple_date == expected


def test_url_for_city():
    print(url_for_city("london"))
    assert "london" in url_for_city("london")
