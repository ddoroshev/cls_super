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
                index = values.index(SUPER)
                for parent in base:
                    parent_values = getattr(parent, attr_name, None)
                    if not parent_values:
                        continue
                    values = values[:index] + parent_values + values[index + 1 :]
                attrs[attr_name] = values
        return super().__new__(cls, name, base, attrs)


class BaseSuper(metaclass=Super):
    _supered_attrs = ["features", "foo"]


class Bar(BaseSuper):
    features = [
        1,
        2,
        3,
    ]


class Baz(Bar):
    features = [
        4,
        5,
    ]


class Eggs(Bar):
    features = [
        4,
        SUPER,
        5,
    ]


class Spam(Eggs):
    features = [SUPER]


def run():
    assert Baz.features == [4, 5], Baz.features
    assert Eggs.features == [4, 1, 2, 3, 5], Eggs.features
    assert Spam.features == [4, 1, 2, 3, 5], Spam.features


if __name__ == "__main__":
    run()
