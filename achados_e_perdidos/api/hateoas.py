class Hateoas:
    def __init__(self):
        self.links = []

    def add_get(self, rel: str, uri: str):
        self.__add("GET", rel, uri)
        
    def add_post(self, rel: str, uri: str):
        self.__add("POST", rel, uri)

    def add_put(self, rel: str, uri: str):
        self.__add("PUT", rel, uri)

    def add_patch(self, rel: str, uri: str):
        self.__add("PATCH", rel, uri)

    def add_delete(self, rel: str, uri: str):
        self.__add("DELETE", rel, uri)

    def __add(self, type, rel: str, uri: str):
        self.links.append({
            'type': type,
            'rel': rel,
            'uri': uri
        })

    def to_array(self):
        return self.links