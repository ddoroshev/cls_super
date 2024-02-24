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
