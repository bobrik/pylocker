__author__ = 'bobrik'

import socket
import struct

class LockerException(Exception): pass
class ConnectionException(LockerException): pass
class InvalidSequenceException(LockerException): pass
class InvalidActionException(LockerException): pass

from .Lock import Lock


class Locker(object):

    ACTION_LOCK = 1

    ACTION_UNLOCK = 0

    REPLY_SIZE = 6

    def __init__(self, host, port = 4545):
        self.host       = host
        self.port       = port
        self.sequence   = 0
        self.connection = None
        self.registry   = {}


    def get_connection(self):
        if self.connection is None:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.host, self.port))

        return self.connection


    def get_next_sequence(self):
        self.sequence += 1
        return self.sequence


    def create_lock(self, name):
        sequence = self.get_next_sequence()
        lock     = Lock(self, name, sequence)

        self.registry[sequence] = lock

        return lock


    def reset(self):
        self.connection = None

        for sequence, lock in self.locks.iteritems():
            if not lock.get_sequence():
                lock.reset()


    def request(self, name, sequence, action, wait, timeout):
        connection = self.get_connection()

        length = len(name)
        buffer = struct.pack("<BIIIB", length, sequence, wait, timeout, action) + name
        if connection.send(buffer) < len(buffer):
            self.connection = None
            self.reset()
            raise ConnectionException("Writing request to locker server failed")

        data = connection.recv(self.REPLY_SIZE)
        (reply_sequence, reply_action, result) = struct.unpack("<IBB", data)

        if reply_sequence != sequence:
            raise InvalidSequenceException("Received invalid sequence in reply")

        if reply_action != action:
            raise InvalidActionException("Received invalid action in reply")

        return result == 1


    def lock(self, name, sequence, wait, timeout):
        return self.request(name, sequence, self.ACTION_LOCK, wait, timeout)


    def unlock(self, sequence):
        return self.request("", sequence, self.ACTION_UNLOCK, 0, 0)


    def unregister(self, lock):
        del self.registry[lock.get_sequence()]
        print self.registry