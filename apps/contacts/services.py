import re

from .models import Contact


def normalize_jid(remote_jid: str) -> str:
    """
    Transforma "5522999999999@s.whatsapp.net" ou "5522999999999@g.us"
    em "5522999999999". Essa é a única função que deve tocar em JID cru
    no sistema inteiro — se amanhã a Evolution mudar o formato, conserta
    aqui e só.
    """
    phone = remote_jid.split("@")[0]
    return re.sub(r"\D", "", phone)


def upsert_contact(remote_jid: str, instance_name: str, push_name: str = "") -> Contact:
    phone = normalize_jid(remote_jid)

    contact, created = Contact.objects.get_or_create(
        phone=phone,
        instance_name=instance_name,
        defaults={"push_name": push_name},
    )

    # Atualiza o nome se veio um novo (perfil pode mudar) sem sobrescrever
    # com vazio, e sempre marca a interação mais recente.
    changed = False
    if push_name and push_name != contact.push_name:
        contact.push_name = push_name
        changed = True
    if changed:
        contact.save(update_fields=["push_name", "last_interaction"])
    else:
        contact.save(update_fields=["last_interaction"])

    return contact
