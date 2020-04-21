#!/usr/bin/env python3
#--------------------------------------------------------------------
#
# Version: 1.0.0
# Date: 11-04-2020
# Author: loet
# Copyright: loet
# License: MIT license
#
#--------------------------------------------------------------------

"""
2048 Game GUI.

"""

import tkinter as tk
import constants
from game import TwentyFortyEight

# Window size constants
WIDTH = 900
HEIGHT = 600

# Main game grid constants
GRID_SIZE = 4
GRID_PADDING = 10


class GameGui(tk.Frame):
    """ Class that runs the game GUI.
    """
    def __init__(self, game, dimensions, theme, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.game = game
        self.dimension = dimensions
        self.theme = theme
        self.grid_cells = []
        self.aspect_ratio = 1.0

        self.bind_keys()

        self.panel_width = self.get_side_panel_width()
        self.init_panels()
        self.init_game_text()
        # self.init_game_score()
        # self.init_game_button()
        self.grid_widget = self.init_grid_widget()

        self.init_grid_cells()
        self.constrain_content(self.grid_widget, self.main_container, self.aspect_ratio)
        self.mainloop()


    def init_panels(self):
        """ Initializes window panels of given width and window height
        Returns a Frame.
        """
        # Left side panel
        if self.panel_width:
            self.side_panel = tk.Frame(bg=self.theme["side_panel"], width=self.panel_width)
            self.side_panel.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Main container
        self.main_container = tk.Frame(bg=self.theme["main_panel"], width=self.dimension["height"])
        self.main_container.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)


    def init_game_text(self):
        """ Initializes the side panel with the Game title and instructions.
        """
        if self.panel_width:
            # Add the title label and instructions.
            title_style = constants.TITLE_FONT
            info_style = constants.TEXT_FONT
            title_width = self.panel_width // 4
            title = tk.Label(master=self.side_panel, text="2048",
                             bg=self.theme["cell_background"][2048],
                             fg=self.theme["cell_color"][2048], justify=tk.CENTER,
                             font=title_style, padx=title_width, pady=title_width)
            title.pack(ipady=10)
            # Add instructions
            info_text = """ Use the arrow keys to \n merge the tiles to \n get the 2048 tile!"""
            info = tk.Label(master=self.side_panel, text=info_text,
                            bg=self.theme["side_panel"],
                            fg=self.theme["side_panel_txt"],
                            justify=tk.CENTER, font=info_style, padx=20, pady=title_width)
            info.pack()


    def init_game_score(self):
        """ Initializes the Game score content.
        """
        if self.panel_width:
            # Add buttons to the panel
            pass


    def init_game_button(self):
        """ Initializes the New Game button.
        """
        if self.panel_width:
            # Add buttons to the panel
            pass


    def key_down(self, event):
        """ Keydown event handler
        """
        direction_name = event.keysym
        if direction_name in constants.DIRECTIONS.keys():
            # Move tiles based on directions, then update display
            value = constants.DIRECTIONS[direction_name]
            self.game.move(value)
            self.update_grid_cells()


    def bind_keys(self):
        """ Bind main arrow key directions to events.
        """
        for name in constants.DIRECTIONS:
            direction = "<" + name + ">"
            self.master.bind(direction, self.key_down)


    def get_side_panel_width(self):
        """ Gets the side panel width.
        Returns the panel width.
        """
        panel_width = self.dimension["width"] - self.dimension["height"]
        if panel_width >= 50:
            return panel_width
        return 0


    def init_grid_widget(self):
        """ Initializes a grid widget frame.
        Returns a Frame.
        """
        # Creates a grid container frame and places in center.
        inner_height = self.dimension["height"] - self.dimension["outer_padding"]
        grid_container = tk.Frame(master=self.main_container, bg=self.theme["grid_background"])
        grid_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER,
                             width=inner_height, height=inner_height)
        return grid_container


    def init_grid_cells(self):
        """ Initializes the grid cells that hold game display values.
        Sets the grid_cell matrix.
        """
        grid_size = self.dimension["grid_size"]
        inner_height = self.dimension["height"] - self.dimension["outer_padding"]
        padding = self.dimension["inner_padding"]
        cell_width = (inner_height - padding * 2) // grid_size
        for i in range(grid_size):
            grid_row = []
            self.grid_widget.rowconfigure(i, weight=1)
            self.grid_widget.columnconfigure(i, weight=1)
            for j in range(grid_size):
                # Get tile value
                num = self.game.get_tile(i, j)
                num_txt = str(num) if num else ""
                # Set cell value and label, append to grid cells.
                cell = tk.Frame(master=self.grid_widget, bg=self.theme["cell_background"][num])
                cell.grid(row=i, column=j, padx=padding, pady=padding)
                content = tk.Label(master=cell, text=num_txt, bg=self.theme["cell_background"][num],
                                   fg=self.theme["cell_color"][num], justify=tk.CENTER,
                                   font=constants.FONT, width=cell_width, height=cell_width)
                content.pack()
                grid_row.append(content)
            self.grid_cells.append(grid_row)


    def constrain_content(self, content_frame, padding_frame, aspect_ratio):
        """ Constrains a content panel within a padding panel based on an
        aspect ratio and a resize event.
        """
        outer_padding = self.dimension["outer_padding"]
        def set_aspect(event):
            """ Resizes the content frame to fit either the width of height
            based on the aspect ratio.
            """
            # Get current widths, check new heights and widths, place window
            desired_width = event.width - outer_padding
            desired_height = int(desired_width / aspect_ratio)
            if desired_height > event.height:
                desired_height = event.height - outer_padding
                desired_width = int(desired_height * aspect_ratio)
            content_frame.place(in_=padding_frame, relx=0.5, rely=0.5,
                                anchor=tk.CENTER, width=desired_width, height=desired_height)
        padding_frame.bind("<Configure>", set_aspect)


    def update_grid_cells(self):
        """ Updates the grid cells with new values from the game.
        """
        total_rows = self.game.get_grid_height()
        total_cols = self.game.get_grid_width()
        for row in range(total_rows):
            for col in range(total_cols):
                # Get new tile, set new background and label
                curr_cell = self.grid_cells[row][col]
                tile = self.game.get_tile(row, col)
                tile_txt = str(tile) if tile != 0 else ""
                curr_cell.configure(text=tile_txt, bg=self.theme["cell_background"][tile],
                                    fg=self.theme["cell_color"][tile])
        self.update_idletasks()


    def start(self):
        """ Start the game
        """
        self.game.reset()


def run_gui():
    """ Instantiate the window and run the main gui.
    """
    root = tk.Tk()
    root.title('2048 Game')
    dimensions = str(WIDTH) + 'x' + str(HEIGHT)
    root.geometry(dimensions)

    # Pass other args
    main_theme = constants.DEFAULT_THEME
    grid_dimensions = {
        "width" : WIDTH,
        "height" : HEIGHT,
        "inner_padding" : GRID_PADDING,
        "outer_padding" : GRID_PADDING * 4,
        "grid_size" : GRID_SIZE
    }

    # New game
    new_game = TwentyFortyEight(GRID_SIZE, GRID_SIZE)

    # Initialize and run the gui
    app = GameGui(new_game, grid_dimensions, main_theme, root)
    app.mainloop()


if __name__ == "__main__":
    run_gui()
