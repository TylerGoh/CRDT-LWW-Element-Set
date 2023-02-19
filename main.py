from datetime import datetime

class LWW_Set:
    def __init__(self):
        self.addition_set = {}
        self.remove_set = {}

    def lookup(self, element):
        if element not in self.addition_set:
            return None
        if element in self.remove_set: # If element is in both sets
            if self.addition_set[element] > self.remove_set[element]: # And addition was the latest entry
                return element
            return None
        return element

    def add(self, element):
        if element not in self.addition_set: #Assert that element does not exist
            datetime_now = datetime.now()
            self.addition_set[element] = datetime.timestamp(datetime_now)
        else:
            raise ValueError

    def remove(self, element):
        if element not in self.remove_set: #Assert that element does not exist
            datetime_now = datetime.now()
            self.remove_set[element] = datetime.timestamp(datetime_now)
        else:
            raise ValueError

    def update_add(self, element):
        if element in self.addition_set: #Assert that element does exist
            datetime_now = datetime.now()
            self.addition_set[element] = datetime.timestamp(datetime_now)
        else:
            raise ValueError

    def update_remove(self, element):
        if element in self.remove_set: #Assert that element does exist
            datetime_now = datetime.now()
            self.remove_set[element] = datetime.timestamp(datetime_now)
        else:
            raise ValueError

def compare(set1,set2):
    if set1.addition_set.keys() <= set2.addition_set.keys(): # If keys in set2's addition_set are a subset of set1's
        if set1.remove_set.keys() <= set2.remove_set.keys(): # Same for remove_set 
            return True
    return False

def mergeDict(dict1,dict2):
    duplicate_keys = set(dict1) & set(dict2) #Convert keys to sets and union
    resolved_dict = {}
    for key in duplicate_keys:
        if(dict1[key]>dict2[key]): #Compare timestamps and store latest timestamp
            resolved_dict[key]= dict1[key]
        else:
            resolved_dict[key]= dict2[key]
    result = dict1.copy()
    result.update(dict2)
    result.update(resolved_dict)
    return result

def merge(set1,set2):
    merged_addition_set = mergeDict(set1.addition_set, set2.addition_set)
    merged_remove_set = mergeDict(set1.remove_set, set2.remove_set)
    return merged_addition_set, merged_remove_set

#Test Cases
def test_update_add():
    element = "foo"
    X = LWW_Set()
    X.add(element)
    timestamp1 = X.addition_set[element]
    X.update_add(element)
    timestamp2 = X.addition_set[element]
    assert (timestamp2 > timestamp1) == True # update_add should update timestamp

def test_update_remove():
    element = "foo"
    X = LWW_Set()
    X.remove(element)
    timestamp1 = X.remove_set[element]
    X.update_remove(element)
    timestamp2 = X.remove_set[element]
    assert (timestamp2 > timestamp1) == True # update_remove should update timestamp


def test_merge():
    element1 = "foo"
    element2 = "bar" 
    X = LWW_Set()
    Y = LWW_Set()
    U = LWW_Set()
    X.add(element1)
    X.add(element2)
    Y.add(element1)
    U.addition_set, U.remove_set = merge(X,Y)
    timestamp1 = X.addition_set[element1]
    timestamp2 = U.addition_set[element1]
    assert (timestamp2 > timestamp1) == True # Merging should keep the key which has the latest timestamp
    
def test_compare():
    element1 = "foo"
    element2 = "bar"
    X = LWW_Set()
    Y = LWW_Set()
    X.add(element1)
    X.add(element2)
    Y.add(element1)
    assert compare(X,Y) == False # Additional elements in X compared to Y should return False
    assert compare(Y,X) == True # Y should be a subset of X
    Y.remove(element1)
    assert compare(Y,X) == False # Y remove_set is no longer a subset of X

def test_lookup():
    element = "foo"
    X = LWW_Set()
    X.add(element)
    X.remove(element)
    assert X.lookup(element) == None # element should be "removed"
    X.update_add(element)
    assert X.lookup(element) == element # Since adding the element was done latest, the element should "exist"

if __name__ == "__main__":
    test_update_add()
    test_update_remove()
    test_merge()
    test_compare()
    test_lookup()