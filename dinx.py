class dinx():
    
    def __init__(self, comp):
        
        assert isinstance(comp, dict), 'Please input a dictionary'
        for x,y in comp.items():
            assert isinstance(x, str), f'Invalid key: {x}. Please input a string, not {type(x).__name__}'
            assert isinstance(y, (list, tuple)), 'Please input lists or tuples'
        
        self._comp = comp
        self._comp_map = [(x,y1) for x,y in self._comp.items() for y1 in y]
    
    def __repr__(self):
        
        return str(self._getall())
    
    def __len__(self):
        
        return len(self._comp_map)
    
    def __getitem__(self, ind):
        
        cls = type(self)

        if isinstance(ind, str):
            if ind in self._comp:
                return cls({ind:self._comp[ind]})
            else:
                raise KeyError(f'No such index: {ind}')
                
        elif isinstance(ind, (list, tuple, set)):
            if all([x in self._comp for x in ind]):
                return cls({x:self._comp[x] for x in ind})
            else:
                raise KeyError(f"The following indices not found: {','.join(filter(lambda x: x not in ind,self._comp))}")
                
        elif isinstance(ind, int): 
            return cls(self._to_dict([self._comp_map[ind]]))
        
        elif isinstance(ind, slice):
            return cls(self._to_dict(self._comp_map[ind]))
        
        else:
            raise TypeError(f"{cls.__name__} indices must be integers, slices or strings")
    
    def __missing__(self, ind):
    
        return None
    
    def __add__(self, other):
        
        assert isinstance(other._comp, dict), 'Please input a dinx'
        _temp = type(self)({x:y[:] for x,y in self._comp.items()})
        _temp += other

        return _temp
    
    def __contains__(self, item):
        
        return item in self._getall()
    
    def __iadd__(self, other):
        
        assert isinstance(other._comp, dict), 'Please input a dinx'
        
        for x,y in filter(lambda x: isinstance(x[1], list), other._comp.items()):
            
            if x in self._comp:
                self._comp[x] += y
            
            else:
                self._comp[x] = y
        
        return self
    
    def __radd__(self, other):
        
        assert isinstance(other._comp, dict), 'Please input a dinx'
        
        if other._comp == {}:
            return self._getall()
        else:
            return self.__add__(self, other)
    
    def __eq__(self, other):
        
        assert isinstance(other, type(self)), 'Please input a dinx'
        
        return self._getall() == other._getall()

    def _sum_lists(self, lists):
        
        lt = []
        for l in lists:
            lt += l
        return lt
    
    def _getall(self):
        
        return self._sum_lists(map(list, self._comp.values()))

    def _to_dict(self, l):

        d_temp = {}

        for x in l:
            if x[0] in d_temp:
                d_temp[x[0]].append(x[1])
            else:
                d_temp[x[0]] = [x[1]]

        return d_temp
    
    def update(self, updates):
        
        assert isinstance(updates, dict), 'Please input a dictionary'
        for y in updates.values():
            assert isinstance(y, (list, tuple)), 'Please input lists or tuples'
        
        self._comp.update(updates)
        self._comp_map = [(x,y1) for x,y in self._comp.items() for y1 in y]
    
    def keys(self):
        
        return list(self._comp.keys())
                            
    def values(self):
        
        return self._getall()
                               
    def struct(self):
        
        return self._comp
    
    def count(self, item):
        
        return self._getall().count(item)
