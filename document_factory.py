from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class Report(Document):
    def render(self) -> str:
        return "Корпоративний звіт: квартальні показники"

class Invoice(Document):
    def render(self) -> str:
        return "Рахунок-фактура #12345. Сума: 10000 UAH"

class Contract(Document):
    def render(self) -> str:
        return "Договір про надання послуг. Сторони: A і B"

class ShadowReport(Document):
    def render(self) -> str:
        return "Тіньовий звіт: квартальні показники (внутрішня версія)"

class ShadowInvoice(Document):
    def render(self) -> str:
        return "Рахунок-фактура #12345. Сума: 15000 UAH. #Примітка: +5000 для кешу"

class ShadowContract(Document):
    def render(self) -> str:
        return "Договір про надання послуг. #Службова інформація: пріоритет високий"

class AbstractDocumentFactory(ABC):
    ALLOWED_TYPES = ['report', 'invoice', 'contract']

    def create(self, doc_type: str) -> Document:
        if doc_type not in self.ALLOWED_TYPES:
            raise ValueError(f"Тип документу '{doc_type}' не дозволено.")
        return self._create_document(doc_type)

    @abstractmethod
    def _create_document(self, doc_type: str) -> Document:
        pass

class CorporateDocumentFactory(AbstractDocumentFactory):
    def _create_document(self, doc_type: str) -> Document:
        if doc_type == 'report':
            return Report()
        elif doc_type == 'invoice':
            return Invoice()
        elif doc_type == 'contract':
            return Contract()

class ShadowDocumentFactory(AbstractDocumentFactory):
    def _create_document(self, doc_type: str) -> Document:
        if doc_type == 'report':
            return ShadowReport()
        elif doc_type == 'invoice':
            return ShadowInvoice()
        elif doc_type == 'contract':
            return ShadowContract()

def get_document_factory(config: dict) -> AbstractDocumentFactory:
    mode = config.get('mode', 'corp')
    if mode == 'shadow':
        return ShadowDocumentFactory()
    return CorporateDocumentFactory()

def client_code(factory: AbstractDocumentFactory, doc_types: list):
    for doc_type in doc_types:
        try:
            document = factory.create(doc_type)
            print(f"Створено '{doc_type}': {document.render()}")
        except ValueError as e:
            print(f"Помилка: {e}")

if __name__ == "__main__":
    document_types_to_create = ['report', 'invoice', 'contract', 'secret_memo']

    print("--- Режим 'corp' ---")
    corp_config = {'mode': 'corp'}
    corp_factory = get_document_factory(corp_config)
    client_code(corp_factory, document_types_to_create)

    print("\n--- Режим 'shadow' ---")
    shadow_config = {'mode': 'shadow'}
    shadow_factory = get_document_factory(shadow_config)
    client_code(shadow_factory, document_types_to_create)
