from tsg.robots_parser import parse_robots
from nose.tools import eq_
robots_test_file_name = 'test/files/robots_test.txt'


def test_parse_robots():
    with open(robots_test_file_name) as robots_file:
        delay, allowed, disallowed = parse_robots(robots_file.read())

    eq_(delay, 1)
    eq_(allowed, ['/db', '/pers', '/rec'])
    eq_(disallowed, ['/cgi-bin/', '/maps/', '/db/indices/', '/pers/xc',
                     '/pers/xk', '/rec/xml'])
