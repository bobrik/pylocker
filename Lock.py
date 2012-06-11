__author__ = 'bobrik'

from .Locker import LockerException


class LockReuseException(LockerException): pass
class LockWaitTimeoutException(LockerException): pass
class UnlockWithoutLockException(LockerException): pass
class LostLockException(LockerException): pass

class Lock(object):

    def __init__(self, locker, name, sequence):
        self.locker   = locker
        self.name     = name
        self.sequence = sequence
        self.acquired = False


    def acquire(self, wait, timeout):
        if self.get_sequence() is None:
            raise LockReuseException("Trying to reuse lock")

        result = self.locker.lock(self.name, self.sequence, wait, timeout)
        if not result:
            raise LockWaitTimeoutException("Wait timeout exceed for lock")

        self.acquired = True


    def release(self, panic = False):
        if not self.is_acquired():
            raise UnlockWithoutLockException("Trying to ulock without lock")

        result = self.locker.unlock(self.sequence)
        self.reset()

        if panic and not result:
            raise LostLockException("Lost lock")


    def reset(self):
        if self.get_sequence():
            self.locker.unregister(self)

        self.sequence = None
        self.acquired = False


    def is_acquired(self):
        return self.acquired


    def get_sequence(self):
        return self.sequence


    def __del__(self):
        if self.is_acquired():
            self.release()
        else:
            if self.get_sequence():
                self.reset()