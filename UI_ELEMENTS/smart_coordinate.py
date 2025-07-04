class SmartCoordinate:
    def __init__(self, value: str | int):

        if type(value) == str:
            self.lst_str_value: list[str] = value.split()
            self._int_value: int = 0
        else:
            self.lst_str_value: list[str] = f"{value}px"
            self._int_value: int = value


    def change_str_value(self, string: str):
        self.lst_str_value = string.split()


    def update_value(self, w_screen, h_screen, w_viewport, h_viewport, w_container, h_container, offset=0) -> None:
        result = 0

        for coord in self.lst_str_value:
            if coord[-2:] == "px":
                result += float(coord[:-2])
            elif coord[-2:] == "vw":
                result += float(coord[:-2]) * w_viewport / 100
            elif coord[-2:] == "vh":
                result += float(coord[:-2]) * h_viewport / 100
            elif coord[-2:] == "sw":
                result += float(coord[:-2]) * w_screen / 100
            elif coord[-2:] == "sh":
                result += float(coord[:-2]) * h_screen / 100
            elif coord[-2:] == "cw":
                result += float(coord[:-2]) * w_container / 100
            elif coord[-2:] == "ch":
                result += float(coord[:-2]) * h_container / 100
            else:
                result += float(coord)
        
        result += offset
        self._int_value = round(result)


    def origin_correction(self, origin: str, size: int, axis: str):
        
        if axis == "x":
            match origin:
                case 'center-up':
                    self._int_value -= size // 2 
                case 'center-center':
                    self._int_value -= size // 2 
                case 'center-down':
                    self._int_value -= size // 2 
                case 'right-up':
                    self._int_value -= size 
                case 'right-center':
                    self._int_value -= size 
                case 'right-down':
                    self._int_value -= size 
                case _:
                    pass
        
        elif axis == "y":
            match origin:
                case 'left-center':
                    self._int_value -= size // 2 
                case 'center-center':
                    self._int_value -= size // 2 
                case 'right-center':
                    self._int_value -= size // 2 
                case 'left-down':
                    self._int_value -= size 
                case 'center-down':
                    self._int_value -= size 
                case 'right-down':
                    self._int_value -= size 
                case _:
                    pass


    @property
    def value(self) -> int:
        return self._int_value