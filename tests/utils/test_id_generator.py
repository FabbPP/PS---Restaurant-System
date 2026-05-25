"""Tests for ID generation uniqueness and isolation."""
from src.utils.id_generator import IdGenerator


def test_id_generator_increments() -> None:
    """PE: Verificar secuencia incremental básica."""
    generator = IdGenerator()
    assert generator.next_id() == 1
    assert generator.next_id() == 2
    assert generator.next_id() == 3

def test_id_generator_isolation() -> None:
    """Invariante: Dos instancias diferentes no deben compartir estado."""
    gen1 = IdGenerator()
    gen2 = IdGenerator()
    
    assert gen1.next_id() == 1
    assert gen2.next_id() == 1
    assert gen1.next_id() == 2
    assert gen2.next_id() == 2
