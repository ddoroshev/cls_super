SUPER = object()


class Super(type):
    def __new__(cls, name, base, attrs):
        inherited_attrs = attrs.get("_inherited_attrs")
        if not inherited_attrs:
            for parent in base:
                inherited_attrs = getattr(parent, "_inherited_attrs", None)
                if inherited_attrs:
                    break

        if not inherited_attrs:
            return super().__new__(cls, name, base, attrs)

        for attr_name in inherited_attrs:
            if SUPER not in attrs.get(attr_name, []):
                continue
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
                    values |= getattr(parent, attr_name, {})
            elif isinstance(values, set):
                values.remove(SUPER)
                for parent in base:
                    values |= getattr(parent, attr_name, set())
            attrs[attr_name] = values
        return super().__new__(cls, name, base, attrs)
