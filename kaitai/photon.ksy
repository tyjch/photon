meta:
  id: photon
  endian: be
  
enums:
  command_types:
    1: acknowledge
    2: connect
    3: verify_connect
    4: disconnect
    5: ping
    6: send_reliable_msg
    7: send_unreliable_msg
    8: send_reliable_frag
  message_types:
    0: unknown
    2: operation_request
    3: message_type_3
    4: event_data
    7: operation_response
    
  
types:
  header:
    seq:
      - id: peer_id
        type: u2
      - id: crc_enabled
        type: u1
      - id: command_count
        type: u1
      - id: timestamp
        type: u4
      - id: challenge
        type: s4
  command:
    seq:
      - id: type
        type: u1
        enum: command_types
      - id: channel_id
        type: u1
      - id: flags
        type: u1
      - id: reserved_byte
        type: u1
      - id: length
        type: s4
      - id: reliable_sequence_number
        type: s4
      - id: data
        type:
          switch-on: type
          cases:
            'command_types::send_reliable_msg': reliable_message
            'command_types::send_reliable_frag': reliable_fragment
            'command_types::send_unreliable_msg': unreliable_message
            'command_types::acknowledge': acknowledge
            'command_types::ping': ping
            'command_types::connect': connect
            'command_types::disconnect': disconnect
            _: u4
  reliable_message:
    seq:
      - id: signature
        type: u1
      - id: type
        type: u1
        enum: message_types
      - id: operation_code
        type: u1
      - id: event_code
        type: u1
      - id: operation_response_code
        type: u2
      - id: operation_debug_byte
        type: u1
      - id: parameter_count
        type: s2
      - id: data
        size: _parent.length - 21
  reliable_fragment:
    seq:
      - id: sequence_number
        type: s4
      - id: fragment_count
        type: s4
      - id: fragment_number
        type: s4
      - id: total_length
        type: s4
      - id: fragment_offset
        type: s4
      - id: data
        size: _parent.length - 32
  unreliable_message:
    seq:
      - id: data
        size: _parent.length - 12
  acknowledge:
    seq:
      - id: data
        size: _parent.length - 12
  ping:
    seq:
      - id: data
        size: _parent.length - 12
  connect:
    seq:
      - id: data
        size: _parent.length - 12
  disconnect:
    seq:
      - id: data
        size: _parent.length - 12
  
  
seq:
  - id: signature
    type: u1
  - id: type
    type: u1
    
  
