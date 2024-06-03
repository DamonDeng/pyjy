import struct

class BinaryReader:
    @staticmethod
    def read_data_to_vector(data, data_type, byte_order_str='='):
        length = len(data)
        length_one = struct.calcsize(data_type)
        count = length // length_one
        
        format_str = byte_order_str + str(count) + data_type
        # print(format_str)
        return struct.unpack(format_str, data)
        # vector.extend(struct.unpack(, data[:length]))

    @staticmethod
    def read_file_to_vector(filename, data_type, byte_order_str='='):
        with open(filename, 'rb') as file:
            data = file.read()
            return BinaryReader.read_data_to_vector(data, data_type, byte_order_str)
