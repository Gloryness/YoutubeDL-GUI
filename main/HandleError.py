class HandleErrors(object):
    def __init__(self, dest, colordef):
        self.exit = exit
        self.destination = dest
        self.color = colordef

    def valid_drive(self):

        if not (not (self.destination is None)
                and not (self.destination == "")
                and self.destination.startswith("R:/") or self.destination.startswith("R:\\")
                or self.destination.startswith("B:/") or self.destination.startswith("B:\\")
                or self.destination.startswith("C:/") or self.destination.startswith("C:\\")
                or self.destination.startswith("B:/") or self.destination.startswith("B:\\")
                or self.destination.startswith("D:/") or self.destination.startswith("D:\\")
                or self.destination.startswith("P:/") or self.destination.startswith("P:\\")
                or self.destination.startswith("U:/") or self.destination.startswith("U:\\")
                or self.destination.startswith("S:/") or self.destination.startswith("S:\\")
                or self.destination.startswith("W:/") or self.destination.startswith("W:\\")
                # You may add as many valid directory's as you want.
                ):

                    print(self.color('1;38;2;255;107;104') + "Invalid destination!")
                    self.exit()

    def valid_end(self):

        if not (not (self.destination is None)
                and not (self.destination == "")
                and self.destination.endswith("/")
                or self.destination.endswith('\\')
                ):
                    print(self.color('1;38;2;255;107;104') + "Must include / or \\ on the end")
                    self.exit()
