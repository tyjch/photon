# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))


class Photon(KaitaiStruct):

    class CommandTypes(Enum):
        acknowledge         = 1
        connect             = 2
        verify_connect      = 3
        disconnect          = 4
        ping                = 5
        send_reliable_msg   = 6
        send_unreliable_msg = 7
        send_reliable_frag  = 8
        command_type        = 12

    class MessageTypes(Enum):
        unknown            = 0
        message_type_1     = 1
        operation_request  = 2
        message_type_3     = 3
        event_data         = 4
        message_type_6     = 6
        operation_response = 7
        message_type_12    = 12

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()


    def _read(self):
        self.interface = self._io.read_bytes(42)
        self.photon = self._root.Header(self._io, self, self._root)
        self.command = [None] * (self.photon.command_count)
        for i in range(self.photon.command_count):
            self.command[i] = self._root.Command(self._io, self, self._root)


    class ReliableFragment(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sequence_number = self._io.read_s4be()
            self.fragment_count = self._io.read_s4be()
            self.fragment_number = self._io.read_s4be()
            self.total_length = self._io.read_s4be()
            self.fragment_offset = self._io.read_s4be()
            self.data = self._io.read_bytes((self._parent.length - 32))


    class Disconnect(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes((self._parent.length - 12))


    class Acknowledge(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes((self._parent.length - 12))


    class ReliableMessage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            try:
                self.signature = self._io.read_u1()
                self.type = self._root.MessageTypes(self._io.read_u1())
                self.operation_code = self._io.read_u1()
                self.event_code = self._io.read_u1()
                self.operation_response_code = self._io.read_u2be()
                self.operation_debug_byte = self._io.read_u1()
                self.parameter_count = self._io.read_s2be()
                self.data = self._io.read_bytes((self._parent.length - 21))
            except EOFError:
                print("ReliableMessage could not be parsed")
                pass


    class Connect(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes((self._parent.length - 12))


    class Command(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._root.CommandTypes(self._io.read_u1())
            self.channel_id = self._io.read_u1()
            self.flags = self._io.read_u1()
            self.reserved_byte = self._io.read_u1()
            self.length = self._io.read_s4be()
            self.reliable_sequence_number = self._io.read_s4be()
            _on = self.type
            if _on == self._root.CommandTypes.send_unreliable_msg:
                self.data = self._root.UnreliableMessage(self._io, self, self._root)
            elif _on == self._root.CommandTypes.send_reliable_msg:
                self.data = self._root.ReliableMessage(self._io, self, self._root)
            elif _on == self._root.CommandTypes.acknowledge:
                self.data = self._root.Acknowledge(self._io, self, self._root)
            elif _on == self._root.CommandTypes.connect:
                self.data = self._root.Connect(self._io, self, self._root)
            elif _on == self._root.CommandTypes.send_reliable_frag:
                self.data = self._root.ReliableFragment(self._io, self, self._root)
            elif _on == self._root.CommandTypes.ping:
                self.data = self._root.Ping(self._io, self, self._root)
            elif _on == self._root.CommandTypes.disconnect:
                self.data = self._root.Disconnect(self._io, self, self._root)
            else:
                self.data = self._io.read_u4be()


    class Ping(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes((self._parent.length - 12))


    class UnreliableMessage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes((self._parent.length - 12))


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.peer_id = self._io.read_u2be()
            self.crc_enabled = self._io.read_u1()
            self.command_count = self._io.read_u1()
            self.timestamp = self._io.read_u4be()
            self.challenge = self._io.read_s4be()



