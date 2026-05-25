from utils.id_generator import IdGenerator


def test_id_generator_increments() -> None:
    generator = IdGenerator()
    assert generator.next_id() == 1
    assert generator.next_id() == 2
