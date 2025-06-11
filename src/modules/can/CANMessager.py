class CANMessager:
    INT_TYPE = 1
    BOOL_TYPE = 2

    def to_two_bytes(self, value: int):
        return (
            (value >> 8) & 0xFF,
            value & 0xFF
        )

    def from_two_bytes(self, bytes: tuple[int, int]):
        (a, b) = bytes
        return (a << 8) | b

    def to_four_bytes(self, value: int):
        return (
            (value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF
        )

    def from_four_bytes(self, value: tuple[int, int, int, int]):
        (a, b, c, d) = value
        return (a << 24) | (b << 16) | (c << 8) | d

    def build_can_message(self, message_id: int, value: int | bool):
        # Message id is serialized as 2 bytes, it can't be bigger
        if (message_id > 0xFFFF):
            raise Exception(f"message_id cannot be greater than {0xFFFF}")

        # Split the message ID into 2 bytes
        # (id_a, id_b) = message_id.to_bytes(2, "big", signed = False)
        (id_a, id_b) = self.to_two_bytes(message_id)

        # Bool check must be before int handling, as bools are ints
        if (isinstance(value, bool)):
            return [id_a, id_b, self.BOOL_TYPE, 0, 0, 0, 0, int(value)]

        # value is serialised as 4 bytes, it can't be bigger
        # this check should probably be different if we're dealing with a signed value?
        if (value < 0 or value > 0xFFFFFFFF):
            raise Exception(f"value must be between 0 and {0xFFFFFFFF}")

        # (vala, valb, valc, vald) = value.to_bytes(4, "big", signed = value_signed)
        (val_a, val_b, val_c, val_d) = self.to_four_bytes(value)

        return [
            # Serialize the id into the first 2 bytes
            id_a, id_b,
            # This byte is used to signify what this value is
            self.INT_TYPE,
            # This byte is not yet used
            0,
            # Serialize the message into the final 4 bytes
            val_a, val_b, val_c, val_d
        ]

    def parse_can_message(self, message: list[int]):
        if (len(message) != 8):
            raise Exception("CAN message MUST be 8 bytes")

        (id_a, id_b, type, ignored, val_a, val_b, val_c, val_d) = message

        id = self.from_two_bytes((id_a, id_b))

        if (type == self.BOOL_TYPE):
            return (id, bool(val_d))

        value = self.from_four_bytes((val_a, val_b, val_c, val_d))

        return (id, value)