import pytest

from cls_super import Super, SUPER


class BaseSuper(metaclass=Super):
    _inherited_attrs = [
        "list_features",
        "tuple_features",
        "dict_features",
        "set_features",
        "features",
    ]


@pytest.mark.parametrize(('base', 'inherited', 'expected'), [
    # list
    ([1, 2, 3], [4, 5, 6], [4, 5, 6]),
    ([1, 2, 3], [SUPER, 4, 5, 6], [1, 2, 3, 4, 5, 6]),
    ([1, 2, 3], [4, 5, 6, SUPER], [4, 5, 6, 1, 2, 3]),
    ([1, 2, 3], [4, SUPER, 5, 6], [4, 1, 2, 3, 5, 6]),
    ([1, 2, 3], [SUPER], [1, 2, 3]),
    # tuple
    ((1, 2, 3), (4, 5, 6), (4, 5, 6)),
    ((1, 2, 3), (SUPER, 4, 5, 6), (1, 2, 3, 4, 5, 6)),
    ((1, 2, 3), (4, 5, 6, SUPER), (4, 5, 6, 1, 2, 3)),
    ((1, 2, 3), (4, SUPER, 5, 6), (4, 1, 2, 3, 5, 6)),
    ((1, 2, 3), (SUPER,), (1, 2, 3)),
    # set
    ({1, 2, 3}, {4, 5, 6}, {4, 5, 6}),
    ({1, 2, 3}, {SUPER, 4, 5, 6}, {1, 2, 3, 4, 5, 6}),
    ({1, 2, 3}, {4, 5, 6, SUPER}, {4, 5, 6, 1, 2, 3}),
    ({1, 2, 3}, {4, SUPER, 5, 6}, {4, 1, 2, 3, 5, 6}),
    ({1, 2, 3}, {SUPER}, {1, 2, 3}),
    # dict
    ({"a": "b", "c": "d"}, {"e": "f"}, {"e": "f"}),
    ({"a": "b", "c": "d"}, {SUPER: "", "e": "f"}, {"a": "b", "c": "d", "e": "f"}),
    ({"a": "b", "c": "d"}, {SUPER: ""}, {"a": "b", "c": "d"}),
])
def test_structures(base, inherited, expected):
    class A(BaseSuper):
        features = base

    class B(A):
        features = inherited

    assert B.features == expected


class BaseSuperFields(metaclass=Super):
    _inherited_attrs = ["fields"]


class User:
    fields = ["first_name", "last_name"]


class UserWithId(User, BaseSuperFields):
    fields = ["id", SUPER]


def test_multiple_inheritance():
    assert UserWithId.fields == ["id", "first_name", "last_name"]
