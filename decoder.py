from kaitai import Photon
from command import Command
import json
from pprint import pprint
from scapy.all import hexdump
from utility import get_hexdump_str

class Decoder(object):

    def __init__(self):
        self.sequences = {}
        self.messages = []

        '''
        sequences = {
            1815: ['blah blah blah', 'bleh bleh bleh', 'blarg, blarg'],
            1816: ['blah blah blah', 'bleh bleh bleh', 'blarg, blarg', None, None]
        }
        '''

    def add_fragment(self, reliable_fragment):
        sequence_number = reliable_fragment.sequence_number
        fragment_number = reliable_fragment.fragment_number
        fragment_count  = reliable_fragment.fragment_count

        # Add a sequence if its sequence_number is not already in the list of sequences
        if sequence_number not in self.sequences.keys():

            # The total number of fragments is contained in each fragment and is used to initialize an empty list
            self.sequences[sequence_number] = [None] * fragment_count

        # Adds a fragments data to a sequence
        self.sequences[sequence_number][fragment_number] = reliable_fragment.data

        # Check if we can decode the sequence
        if self.can_decode(sequence_number):
            messages = self.decode_sequence(sequence_number)
            return messages

    def can_decode(self, sequence_number):
        if None not in self.sequences[sequence_number]:
            return True
        else:
            return False

    def decode_sequence(self, sequence_number):
        list_of_fragments = self.sequences[sequence_number]
        string = b''.join(list_of_fragments)

        header, sep, body = string.partition(b'{')
        string = sep + body

        body, sep, footer = string.rpartition(b'}')
        string = body + sep

        market_entries = [(b'{' + entry)[:-2] for entry in string.split(b'{')]
        market_entries[-1] += b'"}'

        return market_entries[1:]











