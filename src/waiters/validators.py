from src.exceptions.validation import ValidationError

def validate_waiter_name(name: str) -> str:
    """
    Valida que el nombre del mesero contenga únicamente letras y espacios.
    """
    # Verificamos si, al eliminar espacios, el contenido es puramente alfabético
    if not name.replace(" ", "").isalpha():
        raise ValidationError(
            "El nombre del mesero solo debe contener letras y espacios."
        )
    return name