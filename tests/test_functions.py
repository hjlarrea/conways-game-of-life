from components.functions import clicked_button,pos_in_board,return_row_col

def test_clicked_button():
    buttons = {
        "test_button": {
            "id": 1,
            "button": {"x": 650, "y": 250, "width": 100, "height": 50}
        }
    }
    # Clicks inside button coordinates
    assert clicked_button((700,280),buttons) == 1 # Inside
    assert clicked_button((650,250),buttons) == 1 # Upper left corner
    assert clicked_button((750,300),buttons) == 1 # Lower right corner
    assert clicked_button((750,250),buttons) == 1 # Upper right corner
    assert clicked_button((650,300),buttons) == 1 # Lower left corner
    assert clicked_button((650,280),buttons) == 1 # Right margin
    assert clicked_button((680,300),buttons) == 1 # Left margin
    assert clicked_button((700,250),buttons) == 1 # Upper margin
    assert clicked_button((680,300),buttons) == 1 # Lower margin
    # Clicks outside button coordinates
    assert clicked_button((600,240),buttons) == -1 # Outside
    assert clicked_button((650,100),buttons) == -1 # Matching X
    assert clicked_button((100,250),buttons) == -1 # Matching Y

def test_pos_in_board():
    # Positions not in board
    assert pos_in_board((0,0),60) is False
    assert pos_in_board((61,0),60) is False
    assert pos_in_board((0,61),60) is False
    assert pos_in_board((70,70),60) is False
    # Positions in board
    assert pos_in_board((10,10),60) is True
    assert pos_in_board((10,69),60) is True
    assert pos_in_board((69,10),60) is True
    assert pos_in_board((69,69),60) is True

def test_return_row_col():
    pass