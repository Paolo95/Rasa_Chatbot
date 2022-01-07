from typing import Any, Text, Dict, List
import re

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict

VALORI_CONSENTITI_CIRCUITO = ["visa", "mastercard", "diners", "american express", "china union pay"]
VALORI_CONSENTITI_PC = ["notebook", "pc"]
pattern = '([0-9]+( [0-9]+)+)'


class ValidazioneFormOrdine(FormValidationAction):

    def name(self) -> Text:
        return "validate_form_ordine"

    def validate_circuito(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'circuito'."""

        if slot_value.lower() not in VALORI_CONSENTITI_CIRCUITO:
            dispatcher.utter_message(text=f"Si accettano solo i seguenti circuiti: VISA, MASTERCARD, DINERS, AMERICAN EXPRESS, JCB e CHINA UNION PAY")
            return {"circuito":None}
        dispatcher.utter_message(text=f"OK! Il circuito della tua carta di credito è stato accettato!")
        return {"circuito": slot_value}

        return []
    
    def validate_tipologia_prodotto(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'tipologia_prodotto'."""

        if slot_value.lower() not in VALORI_CONSENTITI_PC:
            dispatcher.utter_message(text=f"Si accettano solo ordini relativi a PC e notebook!")
            return {"tipologia_prodotto":None}
        dispatcher.utter_message(text=f"OK!")
        return {"tipologia_prodotto": slot_value}

        return []

    def validate_numero_carta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'numero_carta'."""
        
        if re.match(pattern, slot_value):
            dispatcher.utter_message(text=f"Numero di carta errato, riprova")
            return {"numero_carta":None}
        dispatcher.utter_message(text=f"Il numero della carta è corretto!")
        return {"numero_carta": slot_value}

        return []