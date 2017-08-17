from expiringdict import ExpiringDict
import time
import threading

try:
  from collections import OrderedDict
except ImportError:
  # Python < 2.7
  from ordereddict import OrderedDict

class Expiring(ExpiringDict):
    manage = None

    # Extend contains function to disconnect before deletion
    def __contains__(self, key):
        """ Return True if the dict has a key, else return False. """
        try:
            with self.lock:
                item = OrderedDict.__getitem__(self, key)
                if time.time() - item[1] < self.max_age:
                    return True
                else:
                    print "Removing connection: ", key
                    del self[key]
                    item[0].disconnect()
                    time.sleep(1)
        except KeyError:
            pass
        return False

    # Extend getitem function to refresh timeout on read
    def __getitem__(self, key, with_age=False):
        """ Return the item of the dict.
        Raises a KeyError if key is not in the map.
        """
        with self.lock:
            item = OrderedDict.__getitem__(self, key)
            item_age = time.time() - item[1]
            if item_age < self.max_age:
                item = (item[0],time.time())
                self[key] = item
                if with_age:
                    return item[0], item_age
                else:
                    return item[0]
            else:
                print "Removing connection: ", key
                del self[key]
                item[0].disconnect()
                time.sleep(1)
                raise KeyError(key)  

    def manager(self):
        for key in OrderedDict.keys(self):
            self.__contains__(key)
        self.manage = threading.Timer(self.max_age,self.manager)
        self.manage.daemon = True
        self.manage.start()
