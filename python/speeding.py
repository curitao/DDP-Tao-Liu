def speeding_ticket(speed, is_birthday):
    # Speed limits without birthday
    no_ticket_limit = 60
    small_ticket_limit = 80

    # Speed limits with birthday (increased by 5 mph)
    if is_birthday:
        no_ticket_limit += 5
        small_ticket_limit += 5

    # Check the driver's speed and return the appropriate ticket category
    if speed <= no_ticket_limit:
        return "No Ticket"
    elif speed <= small_ticket_limit:
        return "Small Ticket"
    else:
        return "Big Ticket"

# Example usage:
    
def speeding_ticket(speed, is_birthday):
    # Speed limits without birthday
    no_ticket_limit = 60
    small_ticket_limit = 80

    # Speed limits with birthday (increased by 5 mph)
    if is_birthday:
        no_ticket_limit += 5
        small_ticket_limit += 5

    # Check the driver's speed and return the appropriate ticket category
    if speed <= no_ticket_limit:
        return "No Ticket"
    elif speed <= small_ticket_limit:
        return "Small Ticket"
    else:
        return "Big Ticket"

# Example usage:
print(speeding_ticket(60, False))  # Expected output: "No Ticket"
print(speeding_ticket(75, False))  # Expected output: "Small Ticket"
print(speeding_ticket(85, False))  # Expected output: "Big Ticket"
print(speeding_ticket(65, True))  # Expected output: "No Ticket"
print(speeding_ticket(85, True))  # Expected output: "Small Ticket"
