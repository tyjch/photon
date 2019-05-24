meta:
  id: decoded_message
  file-extension: decoded_message
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

        
seq: 
  - id: msg
    type: reliable_message