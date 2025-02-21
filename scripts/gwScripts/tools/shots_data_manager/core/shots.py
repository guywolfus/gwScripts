
from collections import OrderedDict


class Shots(OrderedDict):
    """
    A data class that defines the shots' information structure.
    """
    name = "shot_name"
    start = "start_frame"
    end = "end_frame"

    def insert_shot(self, row, shot_name, start_frame, end_frame):
        """
        Inserts new shot information as a nested OrderedDict in the given row.

        :param row: The number of the row in the dictionary (`self`) to
            add the new shot to.
        :type row: int

        :param shot_name: The name of the new shot.
        :type shot_name: str

        :param start_frame: The start frame of the new shot.
        :type start_frame: int

        :param end_frame: The end frame of the new shot.
        :type end_frame: int

        :return: Modified dictionary (`self`) with the new shot information
            included in the given row.
        :rtype: Shots
        """
        self[row] = OrderedDict()
        self[row][self.name] = shot_name
        self[row][self.start] = start_frame
        self[row][self.end] = end_frame
        return self

    def get_shot_name(self, row):
        """
        Get a shot's name by row.

        :param row: The row number.
        :type row: int

        :return: The shot's name.
        :rtype: str
        """
        return self[row][self.name]

    def get_shot_start(self, row):
        """
        Get a shot's start frame by row.

        :param row: The row number.
        :type row: int

        :return: The shot's start frame.
        :rtype: int | float
        """
        return self[row][self.start]

    def get_shot_end(self, row):
        """
        Get a shot's end frame by row.

        :param row: The row number.
        :type row: int

        :return: The shot's end frame.
        :rtype: int | float
        """
        return self[row][self.end]
