class ModelMinxi:
    def to_dict(self,*exclude):
        attr_dict = {}
        for field in self._meta.fields:
            name = field.attname
            if name not in exclude:
                attr_dict[name] = getattr(self,name)
        return attr_dict