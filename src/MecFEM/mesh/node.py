class Node:
    """Basic data structure for nodes"""
    def __init__(self,i:int, x:float,y:float,z:float):
        """Create node of label i and coordinates (x,y,z)"""
        self._id = i
        self._X = [x, y, z]

    def __eq__(self, value):
        if isinstance(value, self.__class__):
            if self.id == value.id and self.X == value.X:
                return True
        
        return False

    @property
    def id(self):
        return self._id
    
    @property
    def X(self):
        return self._X
