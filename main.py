SUPER = object()


class Foo(type):
    def __new__(cls, name, base, attrs):
        features = attrs.pop("features", [])
        if SUPER in features:
            index = features.index(SUPER)
            for klass in base:
                klass_features = getattr(klass, "features", None)
                if not klass_features:
                    continue
                features = features[:index] + klass_features + features[index + 1 :]
        return super().__new__(cls, name, base, {**attrs, "features": features})


class Bar(metaclass=Foo):
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
    assert Baz.features == [4, 5], baz.features
    assert Eggs.features == [4, 1, 2, 3, 5], eggs.features
    assert Spam.features == [4, 1, 2, 3, 5], spam.features


if __name__ == "__main__":
    run()
