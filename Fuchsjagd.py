import toga
from toga.style import Pack
from toga.style.pack import ROW, COLUMN, CENTER
from toga.colors import RED, GREEN, WHITE, BLACK, ORANGE,YELLOW
from toga.constants import HIDDEN


class FuchsjagdApp(toga.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_player = 2  # Start with the fox (Fuchs)
        self.button_states = [False] * 30
        self.buttons = []
        self.move_history = []
        self.player_buttons = {1: None, 2: None}
        self.scores = {1: 0, 2: 0}
        self.winner_label = None  # Track the winner label
        self.game_over = False  # Track if the game is over

    def startup(self):
        self.main_window = toga.MainWindow(title="Fuchsjagd")
        main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=10, background_color=BLACK))

        # Title Label
        title_label = toga.Label(
            text="Fuchsjagd",
            style=Pack(padding=(0, 10), font_size=20, color=ORANGE, background_color=BLACK, font_weight='bold', text_align=CENTER)
        )

        # Score Labels
        self.score_label_1 = toga.Label(
            text=f"Punkte Jäger (Rot): {self.scores[1]}",
            style=Pack(padding=10, font_size=15, color=WHITE, background_color=BLACK)
        )
        self.score_label_2 = toga.Label(
            text=f"Punkte Fuchs (Grün): {self.scores[2]}",
            style=Pack(padding=10, font_size=15, color=GREEN, background_color=BLACK)  # Set initial color to green
        )

        # Winner Label
        self.winner_label = toga.Label(
            text="",
            style=Pack(padding=10, font_size=18, color=YELLOW, background_color=BLACK, text_align=CENTER)
        )

        # Score Box
        score_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=(0, 0, 0, 0), background_color=BLACK))
        score_box.add(self.score_label_1)
        score_box.add(self.score_label_2)

        # Outer Box
        outer_box = toga.Box(style=Pack(padding=5, background_color=BLACK))

        # Button Container
        button_container = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=(0, 0, 0, 0), background_color=BLACK))

        # Segment Values
        segment_values = [
            20, 1, 18, 4,
            5, 99, 99, 13,
            12, 99, 99, 6,
            9, 99, 99, 10,
            14, 99, 99, 15,
            11, 99, 99, 2,
            8, 99, 99, 17,
            16, 7, 19, 3
        ]

        # Create Buttons
        for i in range(0, len(segment_values), 4):
            row = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=0, background_color=BLACK))
            for j in range(i, min(i + 4, len(segment_values))):
                button = toga.Button(
                    text=str(segment_values[j]),
                    on_press=self.button_pressed,
                    style=Pack(padding=(5, 5, 5, 5), width=120, height=80, background_color=WHITE, font_size=48, font_weight='bold')
                )
                self.buttons.append(button)
                row.add(button)
            button_container.add(row)

        outer_box.add(button_container)

        # Control Box
        control_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=(0, 5), background_color=BLACK))

        # Control Buttons
        switch_button = toga.Button(
            text="Wechsel",
            on_press=self.switch_player,
            style=Pack(padding=10, width=160, height=60, font_size=24, background_color=WHITE)
        )
        neues_spiel = toga.Button(
            text="Neues Spiel",
            on_press=self.neues_spiel,
            style=Pack(padding=10, width=160, height=60, font_size=24, background_color=WHITE)
        )

        control_box.add(switch_button)
        control_box.add(neues_spiel)

        # Add Elements to Main Box
        main_box.add(title_label)
        main_box.add(score_box)
        main_box.add(self.winner_label)  # Add winner label here
        main_box.add(outer_box)
        main_box.add(control_box)

        # Set Button Visibility
        for index in range(len(self.buttons)):
            if index < len(segment_values) and segment_values[index] == 99:
                self.buttons[index].style.visibility = HIDDEN

        self.main_window.content = main_box
        self.main_window.show()

        # Set initial text color for the current player
        self.update_text_color()

    def button_pressed(self, widget):
        if self.game_over:
            return  # Ignore button presses if the game is over

        index = self.buttons.index(widget)

        # Scoring Logic
        if self.current_player == 1:  # Jäger (Rot)
            if self.player_buttons[1]:  # If there's already a button for player 1
                self.player_buttons[1].style.background_color = WHITE  # Reset previous button
            widget.style.background_color = RED
            self.player_buttons[1] = widget  # Save button for player 1

            # Scoring: Hunter scores if they land on the same field as the fox
            if self.player_buttons[2] == widget:  # Check if the fox pressed the same button
                self.scores[1] += 1  # Hunter scores 1 point
                self.reset_round()

        else:  # Fuchs (Grün)
            if self.player_buttons[2]:  # If there's already a button for player 2
                self.player_buttons[2].style.background_color = WHITE  # Reset previous button
            widget.style.background_color = GREEN
            self.player_buttons[2] = widget  # Save button for player 2

            # Scoring: Fox scores if they land on the field with the number 1
            if int(widget.text) == 1:
                self.scores[2] += 1  # Fox scores 1 point
                self.reset_round()

        # Update Scores
        self.score_label_1.text = f"Punkte Jäger (Rot): {self.scores[1]}"
        self.score_label_2.text = f"Punkte Fuchs (Grün): {self.scores[2]}"

        # Check for Winner
        if self.scores[1] == 2:
            self.winner_label.text = "Jäger (Rot) hat gewonnen!"
            self.game_over = True
        elif self.scores[2] == 2:
            self.winner_label.text = "Fuchs (Grün) hat gewonnen!"
            self.game_over = True

        # Update text color based on current player
        self.update_text_color()

    def reset_round(self):
        # Reset all buttons to white
        for button in self.buttons:
            button.style.background_color = WHITE
        self.player_buttons = {1: None, 2: None}  # Reset player buttons
        self.current_player = 2  # Fox always starts the new round

    def switch_player(self, widget):
        # Switch between player 1 and 2
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_text_color()

    def update_text_color(self):
        if self.current_player == 1:
            self.score_label_1.style.color = RED  # Set text color to red for hunter
            self.score_label_2.style.color = WHITE  # Reset text color for fox
        else:
            self.score_label_1.style.color = WHITE  # Reset text color for hunter
            self.score_label_2.style.color = GREEN  # Set text color to green for fox

    def neues_spiel(self, widget):
        # Reset the game state
        self.button_states = [False] * 30
        for button in self.buttons:
            button.style.background_color = WHITE
        self.move_history = []
        self.player_buttons = {1: None, 2: None}
        self.scores = {1: 0, 2: 0}
        self.score_label_1.text = f"Punkte Jäger (Rot): {self.scores[1]}"
        self.score_label_2.text = f"Punkte Fuchs (Grün): {self.scores[2]}"
        self.winner_label.text = ""
        self.current_player = 2  # Fox always starts
        self.game_over = False  # Reset game over state
        self.update_text_color()  # Reset text color for new game
        
def main():
    return FuchsjagdApp("Fuchsjagd", "org.example.fuchsjagd")


if __name__ == "__main__":
    main().main_loop()