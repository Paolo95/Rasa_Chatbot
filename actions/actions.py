from typing import Any, Text, Dict, List
import re

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict

VALORI_CONSENTITI_CIRCUITO = ["visa", "mastercard", "diners", "american express", "china union pay"]
VALORI_CONSENTITI_PC = ["notebook", "pc"]
pattern_visa = "^4[0-9]{12}(?:[0-9]{3})?$"
pattern_visa_mastercard = "^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$"
pattern_diners = "^3(?:0[0-5]|[68][0-9])[0-9]{11}$"
pattern_mastercard = "^(5[1-5][0-9]{14}|2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12}))$"
pattern_jcb = "^(?:2131|1800|35\d{3})\d{11}$"
pattern_union = "^(62[0-9]{14,17})$"
pattern_intestatario = "^([a-z]+[,.]?[ ]?|[a-z]+['-]?)+$"


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
        string_card = str(slot_value).replace(" ","").replace("-","")
        if re.match(pattern_visa,str(string_card)) or re.match(pattern_visa_mastercard,str(string_card)) is not None:
            dispatcher.utter_message(text=f"Il numero della carta VISA o VISA MASTERCARD è corretto!")
            return {"numero_carta": slot_value}          
        elif re.match(pattern_diners, str(string_card)) is not None:
            dispatcher.utter_message(text=f"Il numero della carta DINERS è corretto!")
            return {"numero_carta": slot_value}
        elif re.match(pattern_mastercard, str(string_card)) is not None:
            dispatcher.utter_message(text=f"Il numero della carta MASTERCARD è corretto!")
            return {"numero_carta": slot_value}
        elif re.match(pattern_jcb, str(string_card)) is not None:
            dispatcher.utter_message(text=f"Il numero della carta JCB è corretto!")
            return {"numero_carta": slot_value}
        elif re.match(pattern_union, str(string_card)) is not None:
            dispatcher.utter_message(text=f"Il numero della carta UNION è corretto!")
            return {"numero_carta": slot_value}
        else:           
            dispatcher.utter_message(text=f"Il numero di carta è errato, riprova")
            return {"numero_carta":None}            
        
    def validate_intestatario_carta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate 'intestatario_carta'."""

        if re.match(pattern_intestatario,str(slot_value)) is not None:
            dispatcher.utter_message(text=f"Inserisci un intestatario valido!")
            return {"intestatario_carta":None}
        dispatcher.utter_message(text=f"OK!")
        return {"intestatario_carta": slot_value}

        return []