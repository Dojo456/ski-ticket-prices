from inspect import signature


# create a decorator to copy signatures
def copy_signature(source_fct):
    def copy(target_fct):
        target_fct.__signature__ = signature(source_fct)
        return target_fct

    return copy
