import ardu_handling

def send_ardu(output_ON):
    actu = ardu_handling.actu()
    actu.update_states()
    if output_ON:   send = ardu_handling.sender()
    else:           send = ardu_handling.sender_txt()
    send.run()