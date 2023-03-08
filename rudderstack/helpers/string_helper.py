class StringHelper:

    @staticmethod
    def get_name(name: str):
        return name.lower().replace(' ', '_')
