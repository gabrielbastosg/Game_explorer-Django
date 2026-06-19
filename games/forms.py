from django.contrib.auth.forms import UserCreationForm


class CadastroForm(UserCreationForm):
    """Igual ao UserCreationForm do Django, mas sem os textos de ajuda
    (regras de senha, etc.). A validação continua acontecendo normalmente —
    só os textos deixam de ser exibidos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
