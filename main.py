SUPER = object()


class Super(type):
    def __new__(cls, name, base, attrs):
        supered_attrs = attrs.get("_supered_attrs")
        if not supered_attrs:
            for parent in base:
                supered_attrs = getattr(parent, "_supered_attrs")
                if supered_attrs:
                    break
        if not supered_attrs:
            return super().__new__(cls, name, base, attrs)

        for attr_name in supered_attrs:
            if SUPER in attrs.get(attr_name, []):
                values = attrs.pop(attr_name)
                if isinstance(values, (list, tuple)):
                    index = values.index(SUPER)
                    for parent in base:
                        parent_values = getattr(parent, attr_name, None)
                        if not parent_values:
                            continue
                        values = values[:index] + parent_values + values[index + 1 :]
                elif isinstance(values, dict):
                    values.pop(SUPER)
                    for parent in base:
                        parent_values = getattr(parent, attr_name, None)
                        if not parent_values:
                            continue
                        values |= parent_values
                attrs[attr_name] = values
        return super().__new__(cls, name, base, attrs)


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
