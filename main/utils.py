def calculate_notes(amount):
    notes = [100, 50, 20, 10, 5, 1]
    note_count = {}

    for note in notes:
        if amount >= note:
            count = amount // note
            amount %= note # Replace amount with remainder
            note_count[note] = count

    return note_count