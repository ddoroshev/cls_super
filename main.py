from cls_super import Super, SUPER


class BaseSuper(metaclass=Super):
    _supered_attrs = [
        "list_features",
        "dict_features",
    ]


class Bar(BaseSuper):
    list_features = [
        1,
        2,
        3,
    ]

    dict_features = {
        "a": "b",
        "c": "d",
    }


class Baz(Bar):
    list_features = [
        4,
        5,
    ]
    dict_features = {
        "e": "f",
    }


class Eggs(Bar):
    list_features = [
        4,
        SUPER,
        5,
    ]
    dict_features = {
        SUPER: "",
        "e": "f",
    }


class Spam(Eggs):
    list_features = [SUPER]
    dict_features = {SUPER: ""}


def run():
    assert Baz.list_features == [4, 5], Baz.list_features
    assert Baz.dict_features == {"e": "f"}, Baz.dict_features
    assert Eggs.list_features == [4, 1, 2, 3, 5], Eggs.list_features
    assert Eggs.dict_features == {"a": "b", "c": "d", "e": "f"}, Eggs.dict_features
    assert Spam.list_features == [4, 1, 2, 3, 5], Spam.list_features
    assert Spam.dict_features == {"a": "b", "c": "d", "e": "f"}, Spam.dict_features


if __name__ == "__main__":
    run()
