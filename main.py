from cls_super import Super, SUPER


class BaseSuper(metaclass=Super):
    _inherited_attrs = [
        "list_features",
        "tuple_features",
        "dict_features",
        "set_features",
    ]


class Bar(BaseSuper):
    list_features = [1, 2, 3]
    tuple_features = (1, 2, 3)
    set_features = {1, 2, 3}
    dict_features = {"a": "b", "c": "d"}


class Baz(Bar):
    list_features = [4, 5]
    tuple_features = (4, 5)
    set_features = {4, 5}
    dict_features = {"e": "f"}


class Eggs(Bar):
    list_features = [
        4,
        SUPER,
        5,
    ]
    tuple_features = (
        4,
        SUPER,
        5,
    )
    set_features = {
        4,
        SUPER,
        5,
    }
    dict_features = {
        SUPER: "",
        "e": "f",
    }


class Spam(Eggs):
    list_features = [SUPER]
    dict_features = {SUPER: ""}


class BaseSuperFields(metaclass=Super):
    _inherited_attrs = ["fields"]


class User:
    fields = ["first_name", "last_name"]


class UserWithId(User, BaseSuperFields):
    fields = ["id", SUPER]


def run():
    assert Baz.list_features == [4, 5], Baz.list_features
    assert Baz.tuple_features == (4, 5), Baz.tuple_features
    assert Baz.set_features == {4, 5}, Baz.set_features
    assert Baz.dict_features == {"e": "f"}, Baz.dict_features
    assert Eggs.list_features == [4, 1, 2, 3, 5], Eggs.list_features
    assert Eggs.tuple_features == (4, 1, 2, 3, 5), Eggs.tuple_features
    assert Eggs.set_features == {4, 1, 2, 3, 5}, Eggs.set_features
    assert Eggs.dict_features == {"a": "b", "c": "d", "e": "f"}, Eggs.dict_features
    assert Spam.list_features == [4, 1, 2, 3, 5], Spam.list_features
    assert Spam.tuple_features == (4, 1, 2, 3, 5), Spam.tuple_features
    assert Spam.set_features == {4, 1, 2, 3, 5}, Spam.set_features
    assert Spam.dict_features == {"a": "b", "c": "d", "e": "f"}, Spam.dict_features

    assert User.fields == ["first_name", "last_name"], User.fields
    assert UserWithId.fields == ["id", "first_name", "last_name"], UserWithId.fields


if __name__ == "__main__":
    run()
