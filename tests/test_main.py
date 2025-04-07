from src.main import main

def test_main_runs():
    
    try:
        main()
    except Exception as e:
        assert False, f"main() raised an exception: {e}"

def test_get_x():
    assert get_x(19) == "big 20"