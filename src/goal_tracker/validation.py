from pydantic import ValidationError


def validation_message(error: ValidationError) -> str:
    fields = sorted({str(item["loc"][0]) for item in error.errors() if item.get("loc")})
    if not fields:
        return "Please check your goal details."
    labels = ", ".join(field.replace("_", " ").title() for field in fields)
    return f"Please correct: {labels}."
