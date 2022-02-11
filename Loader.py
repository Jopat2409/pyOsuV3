

import threading



class ThreadVar:

    def __init__(self, _type, value=None):
        self.m_rValue = value
        self.m_lock = threading.Lock()
        self.m_vType = _type

    def GetValue(self):
        with self.m_lock:
            return self.m_rValue
        return None

    def SetValue(self, value):
        with self.m_lock:
            self.m_rValue = value
            return True
        return False



class Loader(threading.Thread):

    def __init__(self, rType):
        self.m_rType = rType
        self.m_rValue = ThreadVar(self.m_rType)
        super(Loader, self).__init__()
        self.start()
        
    def run(self):

        t_value = self.Load()
        while not self.m_rValue.SetValue(t_value):
            self.m_rValue.SetValue(t_value)

    def Load(self):
        raise NotImplementedError
