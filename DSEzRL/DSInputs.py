class DSInputs: 
    def __init__(self, a = False, b = False, x = False, y = False, up = False, down = False, left = False, right = False,
                start = False, select = False, l = False, r = False, touch = (0, 0, False)) -> None:
        # Buttons
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        # D-Pad
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        
        # Start and Select
        self.start = start
        self.select = select

        # Triggers
        self.l = l
        self.r = r

        # Touch screen, starting from top left --> X(255 max), Y(191 max), Pressed
        self.touch = touch
    
    def to_instructions(self): 
        keymap = [self.a, self.b, self.select, self.start, self.right, self.left, self.up, self.down, self.r, self.l, self.x, self.y]
        instructions = [] 
        for i in range(0, len(keymap)) : 
            instructions.append((i+1, keymap[i]))

        return instructions


