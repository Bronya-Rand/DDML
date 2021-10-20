
default persistent.custom = False

init -1 python:
    if persistent.custom:
        # The color of non-interactive text.
        TEXT = "#545454"

        # Colors for buttons in various states.
        IDLE = "#42637b"
        HOVER = "#d86b45"
        DISABLED = "#808080"

        # Colors for reversed text buttons (selected list entries).
        REVERSE_IDLE = "#78a5c5"
        REVERSE_HOVER = "#d86b45"
        REVERSE_TEXT = "#ffffff"

        # Colors for the scrollbar thumb.
        SCROLLBAR_IDLE = "#dfdfdf"
        SCROLLBAR_HOVER = "#d86b45"

        # An image used as a separator pattern.
        PATTERN = "images/pattern_custom.png"

        # A displayable used for the background of everything.
        BACKGROUND = "images/background_custom.png"

        # A displayable used for the background of windows
        # containing commands, preferences, and navigation info.
        WINDOW = Frame("images/window_custom.png", 0, 0, tile=True)

        # A displayable used for the background of the projects list.
        PROJECTS_WINDOW = Null()

        # A displayable used the background of information boxes.
        INFO_WINDOW = "#f9f9f9"

        # Colors for the titles of information boxes.
        ERROR_COLOR = "#d15353"
        INFO_COLOR = "#545454"
        INTERACTION_COLOR = "#d19753"
        QUESTION_COLOR = "#d19753"

        # The color of input text.
        INPUT_COLOR = "#d86b45"
