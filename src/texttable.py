"""
TextTable is use to generate a pretty table in text format, 
which can be easily printed on console or output into text file

Sample:
Name  Age  Gender  Desc                  Nationality
You   10   male    You are a boy         China
Me    100  male    I am an old man       Japan
She   18   female  She is a pretty girl  America
He    1    male    He is a little baby   British
"""

import textwrap
from exceptions import Error

class TextTable(object):

    def __init__(self, field_names, **kwargs):
        '''
        Arguments:
        field_names - list or tuple of field names
        vertical_str - vertical separator betwwen each columns
        '''
        self._field_names = field_names
        self._rows = []
        self._sequence = [False, '', 0]
        self._max_widths = {}
        self._vertical_str = '  '
        self._padding_width = 0

        supported_options = ('vertical_str',)
        for key, value in kwargs.items():
            if key not in supported_options:
                raise Error('unsupported option: ' + key)
            setattr(self, '_'+key, value)

    def set_sequence(self, enable, field_name='Seq', start=1):
        '''
        set whether need sequence for each row.

        Arguments:
        enable - whether need sequence for each row
        field_name - the name of sequence field
        start - the start number of sequence
        '''
        self._sequence = [enable, field_name, start]

    def set_max_width(self, field_name, max_width):
        '''
        set max width of sepcified column, if max width is shorter than the length of field name,
        the max width will be the length of field name

        Arguments:
        field_name - specify the field
        max_width - max width of the specified field
                    if the actual value exceed the max width, will be split in multiple lines
        '''
        self._max_widths[field_name] = max_width

    def _format_rows(self, rows):
        '''
        convert each column to string
        '''
        formatted_rows = []
        for index, row in enumerate(rows):
            formatted_row = [str(col) for col in row]
            if self._sequence[0]:
                formatted_row.insert(0, str(index+self._sequence[2]))
            formatted_rows.append(formatted_row)
        return formatted_rows

    def _calculate_widths(self, field_names, rows):
        '''
        calculate max width of each column
        '''
        widths = [len(field) for field in field_names]
        for row in rows:
            for index, value in enumerate(row):
                lines = value.split('\n')
                max_len = max([len(line) for line in lines])
                field_name = field_names[index]
                if field_name in self._max_widths:
                    widths[index] = max(widths[index], min(max_len, self._max_widths[field_name]))
                else:
                    widths[index] = max(widths[index], max_len)
        return widths
    def _get_row_string(self, field_names, row, widths):
        '''
        get formatted row string
        '''
        lines = []
        total_width = 0
        padding = self._padding_width * ' '
        for index, field, value, width, in zip(range(0, len(row)), field_names, row, widths):
            last_column = True if index == len(row) - 1 else False
            col_lines = value.split('\n')
            final_col_lines = []
            for line in col_lines:
                final_col_lines += textwrap.wrap(line, width)
            for index, line in enumerate(final_col_lines):
                if len(lines) <= index:
                    column = total_width*' ' + line + (width-len(line))*' '
                    lines.append(padding + column + padding)
                    if not last_column:
                        lines[index] += self._vertical_str
                else:
                    column = (total_width-len(lines[index]))*' ' + line + (width-len(line))*' '
                    lines[index] += padding + column + padding
                    if not last_column:
                        lines[index] += self._vertical_str
            total_width += width + self._padding_width*2 + len(self._vertical_str)
        return '\n'.join(lines)

    def to_string(self, ignore_field_names=False):
        '''
        get formatted result
        '''
        return '\n'.join(self.to_lines(ignore_field_names))

    def to_lines(self, ignore_field_names=False):
        '''
        get formatted result
        '''
        field_names = [self._sequence[1]] + list(self._field_names) if self._sequence[0] else self._field_names
        formatted_rows = self._format_rows(self._rows)
        widths = self._calculate_widths(field_names, formatted_rows)
        lines = []
        if not ignore_field_names:
            lines.append(self._get_row_string(field_names, field_names, widths))
        for row in formatted_rows:
            lines.append(self._get_row_string(field_names, row, widths))
        return lines

    def add_row(self, row):
        '''
        Arguments:
        row - list or tuple of field values
        '''
        if len(row) != len(self._field_names):
            raise Error("Row has different number of values with field names, (row) %d!=%d (field)" \
                    % (len(row), len(self._field_names)))
        new_row = [col if col is not None else '' for col in row]
        self._rows.append(new_row)

    def add_rows(self, rows):
        for row in rows:
            self.add_row(row)

if __name__ == "__main__":
    table = TextTable(['Name', 'Age', 'Gender', 'Desc', 'Nationality'], vertical_str='  ')
    table.add_row(('You', 10, 'male', 'You are a boy', 'China'))
    table.add_row(('Me', 100, 'male', 'I am an old man', 'Japan'))
    table.add_row(('She', 18, 'female', 'She is a pretty girl', 'America'))
    table.add_row(('He', 1, 'male', 'He is a little baby', 'British'))
    #table.set_sequence(True)
    print(table.to_string())
